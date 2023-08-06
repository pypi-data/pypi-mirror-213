from datetime import datetime
from math import floor, log10, pi
from uuid import UUID

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from bert_schemas import job as job_schema
from matplotlib.ticker import FormatStrFormatter, LinearLocator
from pydantic import Field

from oqtant.util.exceptions import (
    JobPlotFitError,
    JobPlotFitMismatchError,
    JobReadError,
)

OMEGA_X = 2 * pi * 80
OMEGA_Y = 2 * pi * 1000


def round_sig(x: float, sig: int = 2):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def TF_dist_2D(xy_mesh, TFpOD, xc, yc, rx, ry, os):
    """
    Defines 2D Thomas-Fermi distribution characteristic of zero-temperature Bose-gas
    Requires function(s): get_image_space
    :param xy_mesh:
    :type xy_mesh: (2,N,M) Matrix of floats containing mesh grid of image coordinates
    :param TFpOD:
    :type TFpOD: float - Thomas-Fermi peak Optical Density (OD)
    :param rx:
    :type rx: float - Thomas-Fermi radius along the x-direction
    :param ry:
    :type ry: float - Thomas-Fermi radius along the y-direction (along gravity)
    :param xc:
    :type xc: float - Cloud center along the x-direction (along gravity)
    :param yc:
    :type yc: float - Cloud center along the y-direction
    :param os:
    :type os: float - Constant offset
    """

    # unpack 1D list into 2D x and y coords
    (x, y) = xy_mesh

    # Simplify Thomas-Fermi expression
    A = 1 - ((y - yc) / rx) ** 2 - ((x - xc) / ry) ** 2

    # make 2D Thomas-Fermi distribution
    OD = np.real(TFpOD * np.maximum(np.sign(A) * (np.abs(A)) ** (3 / 2), 0)) + os

    # flatten the 2D Gaussian down to 1D
    return OD.ravel()


def Gaussian_dist_2D(xy_mesh, GpOD, xc, yc, sigx, sigy, os):
    """
    Defines 2D gaussian distribution characteristic of a thermal ensemble of atoms
    Requires function(s): get_image_space
    :param xy_mesh:
    :type xy_mesh: (2,N,M) Matrix of floats containing meshgrid of image coordinates
    :param GpOD:
    :type GpOD: float - Gaussian peak Optical Density (OD)
    :param sigx:
    :type sigx: float - Gaussian spread along the x-direction
    :param sigy:
    :type sigy: float - Gaussian spread along the y-direction (along gravity)
    :param xc:
    :type xc: float - Cloud center along the x-direction (along gravity)
    :param yc:
    :type yc: float - Cloud center along the y-direction
    :param os:
    :type os: float - Constant offset
    """

    (x, y) = xy_mesh

    OD = (
        GpOD * np.exp(-0.5 * ((y - yc) / sigy) ** 2 - 0.5 * ((x - xc) / sigx) ** 2) + os
    )
    return OD.ravel()


def bimodal_dist_2D(xy_mesh, GpOD, sigx, sigy, TFpOD, rx, ry, xc, yc, os):
    """
    Defines 2D bimodal distribution characteristic of finite-temperature Bose-gas
    Requires functions: Gaussian_dist_2D, TF_dist_2D, get_image_space
    :param xy_mesh:
    :type xy_mesh: (2,N,M) Matrix of floats containing meshgrid of image coordinates
    :param GpOD:
    :type GpOD: float - Gaussian peak Optical Density (OD)
    :param sigx:
    :type sigx: float - Gaussian spread along the x-direction
    :param sigy:
    :type sigy: float - Gaussian spread along the y-direction (along gravity)
    :param TFpOD:
    :type TFpOD: float - Thomas-Fermi peak Optical Density (OD)
    :param rx:
    :type rx: float - Thomas-Fermi radius along the x-direction
    :param ry:
    :type ry: float - Thomas-Fermi radius along the y-direction (along gravity)
    :param xc:
    :type xc: float - Cloud center along the x-direction (along gravity)
    :param yc:
    :type yc: float - Cloud center along the y-direction
    :param os:
    :type os: float - Constant offset
    """

    return Gaussian_dist_2D(xy_mesh, GpOD, xc, yc, sigx, sigy, os) + TF_dist_2D(
        xy_mesh, TFpOD, xc, yc, rx, ry, os
    )


class OqtantJob(job_schema.JobCreate):
    external_id: UUID | None
    time_submit: datetime | None
    pix_cal: float = Field(8.71, const=True)
    sig_abs: float = Field(0.297, const=True)
    omega_x: float = Field(OMEGA_X, const=True)
    omega_y: float = Field(OMEGA_Y, const=True)

    class Config:
        validate_assignment = True

    def get_TOF(self):
        """
        Returns shaped TOF image if it exists
        :returns: reshaped pixels numpy array (100,100)

        """
        if self.status != job_schema.JobStatus.COMPLETE:
            raise JobReadError("Job results not available.")
        try:
            reshaped_pixels = np.array(
                self.inputs[0].output.values.tof_image.pixels
            ).reshape(100, 100)
        except Exception as exc:
            raise JobReadError("no TOF results") from exc
        return reshaped_pixels

    def get_IT(self):
        """
        Returns shaped IT image if it exists
        :returns: reshaped pixels numpy array (100,100)

        """
        if self.status != job_schema.JobStatus.COMPLETE:
            raise JobReadError("Job results not available.")

        try:
            reshaped_pixels = np.array(
                self.inputs[0].output.values.it_plot.pixels
            ).reshape(148, 512)
        except Exception as exc:
            raise JobReadError("no IT results") from exc
        return reshaped_pixels

    @staticmethod
    def get_image_space(datafile=np.zeros((100, 100)), centered="y"):
        """
        Returns meshgrid of image coordinates
        :param datafile:
        :type datafile: (N,M) Matrix of Optical Density (OD) Data
        """

        lx, ly = np.shape(datafile)
        x, y = np.arange(lx), np.arange(ly)

        if centered == "y":
            x = x - round(lx / 2)
            y = y - round(ly / 2)

        xy_mesh = np.meshgrid(x, y)

        return xy_mesh, lx, ly

    def fit_bimodal_data2D(self, xi=None, lb=None, ub=None):
        """
        Performs fit via trust region reflective algorithm.
        Requires functions: bimodal_dist_2D, Gaussian_dist_2D, TF_dist_2D, get_image_space
        For better fit performance, tune initial guess 'xi' and lower/upper bounds, 'lb' and 'ub'
        :param xy_mesh:
        :type xy_mesh: (2,N,M) Matrix containing meshgrid of image data coordinates
        :param data2D:
        :type data2D: (N,M) Matrix containing image data
        :param xi:
        :type xi: (1,9) List of fit parameter initial guesses
        :param lb:
        :type lb:  (1,9) List of fit parameter lower bounds
        :param ub:
        :type ub: (1,9) List of fit parameter upper bounds
        """
        xi = xi if xi else [0.25, 8, 8, 1, 4, 6, 0, 0, 0.02]
        lb = lb if lb else [0, 7, 7, 0, 2, 2, -20, -20, 0]
        ub = ub if ub else [2, 20, 20, 2, 20, 20, 20, 20, 1]

        TOF_data = self.get_TOF()
        xy_mesh, _, _ = self.get_image_space()  # TOF_data)

        (X, Y) = xy_mesh
        x = X[0]
        y = Y[:, 0]

        fit_params, cov_mat = opt.curve_fit(
            bimodal_dist_2D, xy_mesh, np.ravel(TOF_data), p0=xi, bounds=(lb, ub)
        )
        fit_residual = TOF_data - bimodal_dist_2D(xy_mesh, *fit_params).reshape(
            np.outer(x, y).shape
        )
        fit_Rsquared = 1 - np.var(fit_residual) / np.var(TOF_data)

        return fit_params, cov_mat, fit_residual, fit_Rsquared

    def plot_fit_results(
        self, fit_params, model="bimodal", file_name=None, plot_title=None
    ):
        """
        Plot the results of a fit operation

        :param fit_params:
        :type fit_params: list of parameters from a fit operation
        :param model:
        :type model: string "bimodal", "TF", or "gaussian". default "bimodal"
        :param output:
        :type output: valid filename
        :param plot_title:
        :type plot_title: string title for the plot.
            default "job: "+str(self.name)+"\nTOF fit: "+str(model)

        """

        xy_mesh, _, _ = self.get_image_space()  # TOF_data)

        (X, Y) = xy_mesh

        if model == "bimodal":
            try:
                m = bimodal_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise JobPlotFitMismatchError() from exc
            except Exception as exc:
                raise JobPlotFitError() from exc

        elif model == "gaussian":
            try:
                m = Gaussian_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise TypeError(
                    "PLOT FIT RESULTS: mismatched parameters and model type"
                ) from exc
            except Exception as exc:
                raise JobPlotFitError() from exc
        elif model == "TF":
            try:
                m = TF_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise JobPlotFitMismatchError() from exc
            except Exception as exc:
                raise JobPlotFitError() from exc
        else:
            print(
                f"PLOT FIT RESULTS: Invalid model specified: {model}.",
                " Select 'bimodal', 'gaussian', or 'TF'",
            )
            return

        m = m.reshape(100, 100)
        plt.figure()
        plt.imshow(
            m,
            origin="lower",
            cmap="nipy_spectral",
            extent=[
                np.min(X) * self.pix_cal,
                np.max(X) * self.pix_cal,
                np.min(Y) * self.pix_cal,
                np.max(Y) * self.pix_cal,
            ],
        )

        if plot_title is None:
            plot_title = f"job: {self.name}\nTOF fit: {model}"

        plt.title(plot_title)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    @staticmethod
    def _save_plot_file(plot, file_name):
        file = f"{file_name}.png"
        try:
            plot.savefig(file)
            print(f"plot saved to file: {file}")
        except (FileNotFoundError, Exception):
            print(f"failed to save plot at {file}")

    def atoms_2dplot(self, file_name=None, figsize=(12, 12), gridon=False):
        """
        Generate a 2D plot of atom OD (save or show)

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param figsize:
        :type figsize: tuple. default is (12,12)
        :param gridon: grid lines on plot on/off
        :type gridon: Boolean. default is False

        """

        TOF_data = self.get_TOF()
        xy_mesh, _, _ = self.get_image_space()  # TOF_data)
        (X, Y) = xy_mesh

        fig2D = plt.figure(figsize=figsize)
        ax = fig2D.gca()
        plt2D = plt.imshow(
            TOF_data,
            origin="lower",
            cmap="nipy_spectral",
            extent=[
                np.min(X) * self.pix_cal,
                np.max(X) * self.pix_cal,
                np.min(Y) * self.pix_cal,
                np.max(Y) * self.pix_cal,
            ],
        )
        plt.grid(b=gridon)
        plt.colorbar(plt2D, shrink=0.8)

        ax.set_xlabel("x-position, micron", labelpad=15, fontsize=16)
        ax.set_ylabel("y-position, micron", labelpad=15, fontsize=16)
        plt.title("Time of Flight Optical Depth", fontsize=16)

        print("Peak OD: ", np.max(TOF_data))

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    def atoms_sliceplot(self, file_name=None, sliceaxis="x", gridon=False):
        """
        Generate a 1D slice plot of atom OD in x or y

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param sliceaxis:
        :type sliceaxis: string 'x' or 'y'
        :param figsize:
        :type figsize: tuple. default is (12,12)
        :param gridon: grid lines on plot on/off
        :type gridon: Boolean. default is False

        """
        TOF_data = self.get_TOF()
        xy_mesh, lx, ly = self.get_image_space(TOF_data)
        (X, Y) = xy_mesh

        params, *_ = self.fit_bimodal_data2D()
        fitOD = bimodal_dist_2D(xy_mesh, *params)

        Gfit_params = [params[0], params[6], params[7], params[1], params[2], params[8]]
        fitODG = Gaussian_dist_2D(xy_mesh, *Gfit_params)

        # Reshape Fit Distributions to 2D form
        fitOD2D = fitOD.reshape(lx, ly)
        fitODG2D = fitODG.reshape(lx, ly)

        # Define Central slices
        xslice = fitOD2D[int(lx / 2), :]
        yslice = fitOD2D[:, int(ly / 2)]
        xsliceG = fitODG2D[int(lx / 2), :]
        ysliceG = fitODG2D[:, int(ly / 2)]

        if sliceaxis == "x":
            xsliceD = TOF_data[int(len(X[1]) / 2), :]
            xslice = fitOD2D[int(len(X[1]) / 2), :]
            xsliceG = fitODG2D[int(len(X[1]) / 2), :]
            plt.title("X-Slice", fontsize=16)
            plt.plot(X[1] * self.pix_cal, xsliceD, "ok")
            plt.plot(X[1] * self.pix_cal, xslice, "b")
            plt.plot(X[1] * self.pix_cal, xsliceG, "r")
        elif sliceaxis == "y":
            ysliceD = TOF_data[:, int(len(Y[1]) / 2)]
            yslice = fitOD2D[:, int(len(Y[1]) / 2)]
            ysliceG = fitODG2D[:, int(len(Y[1]) / 2)]
            plt.title("Y-Slice", fontsize=16)
            plt.plot(Y[:, 1] * self.pix_cal, ysliceD, "ok")
            plt.plot(Y[:, 1] * self.pix_cal, yslice, "b")
            plt.plot(Y[:, 1] * self.pix_cal, ysliceG, "r")
        else:
            raise ValueError("Input either x or y")

        plt.grid(b=gridon)
        plt.xlabel("x-position, micron", labelpad=15, fontsize=16)
        plt.ylabel("Optical Depth", labelpad=15, fontsize=16)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    # This function plots the optical depth as a 3D surface with projected density contours
    def atoms_3dplot(self, file_name=None, view_angle=-45, figsize=(10, 10)):
        """
        Generate a 3D slice plot of atom OD

        :param output: how to output the information
        :type output: string "show" or valid filename
        :param view_angle:
        :type view_angle: int (-180, 180). default -45
        :param figsize:
        :type figsize: tuple. default is (10,10)

        """

        fig3d = plt.figure(figsize=figsize)
        ax = fig3d.gca(projection="3d")

        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        # Set axis labels
        ax.set_xlabel("x-position, micron", labelpad=10)
        ax.set_ylabel("y-position, micron", labelpad=10)
        ax.set_zlabel("Optical Depth", labelpad=10)

        # rotate the axes and update
        ax.view_init(30, view_angle)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    def atom_numbers(self, bimodalfit_params, print_results=True):
        xy_mesh, lx, ly = self.get_image_space()

        # lmfit Toolbox Results
        # Remove Background
        bimodalfit_params[8] = bimodalfit_params[8] * 0

        # Define Fit Distributions in 1D form
        fitOD = bimodal_dist_2D(xy_mesh, *bimodalfit_params)
        Gfit_params = [
            bimodalfit_params[0],
            bimodalfit_params[6],
            bimodalfit_params[7],
            bimodalfit_params[1],
            bimodalfit_params[2],
            bimodalfit_params[8],
        ]
        TFfit_params = [
            bimodalfit_params[3],
            bimodalfit_params[6],
            bimodalfit_params[7],
            bimodalfit_params[4],
            bimodalfit_params[5],
            bimodalfit_params[8],
        ]
        fitODG = Gaussian_dist_2D(xy_mesh, *Gfit_params)
        fitODTF = TF_dist_2D(xy_mesh, *TFfit_params)
        lmfitbg = lx * ly * bimodalfit_params[8]

        # Reshape Fit Distributions to 2D form
        fitOD2D = fitOD.reshape(lx, ly)
        fitODG2D = fitODG.reshape(lx, ly)
        fitODTF2D = fitODTF.reshape(lx, ly)

        ODsumtot = np.sum(fitOD2D) - lmfitbg * 2
        ODsumcond = np.sum(fitODTF2D) - lmfitbg
        ODsumtherm = np.sum(fitODG2D) - lmfitbg
        Ncond = self.pix_cal**2 / self.sig_abs * ODsumcond  # Condensed atom number
        Ntherm = self.pix_cal**2 / self.sig_abs * ODsumtherm  # Thermal atom  number
        Ntot = self.pix_cal**2 / self.sig_abs * ODsumtot  # Thermal atom  number

        if print_results:
            print("Total Atom Number: ", int(Ntot))
            print("Condensed Atom Number: ", int(Ncond))
            print("Thermal Atom Number: ", int(Ntherm))

        return [Ntot, Ncond, Ntherm]

    def calculate_temperature(self, bimodalfit_params):
        Gfit_params = [
            bimodalfit_params[0],
            bimodalfit_params[6],
            bimodalfit_params[7],
            bimodalfit_params[1],
            bimodalfit_params[2],
            bimodalfit_params[8],
        ]

        TOF = 0
        TOF = self.input.time_of_flight_ms * 1e-3
        # Time of flight
        tau_x = self.omega_x * TOF  # Dimensionless expansion coefficient
        tau_y = self.omega_y * TOF
        pixcal = 8.71 * 1e-6
        # pixel calibration - input sizes as # of pixels
        mRb = 87 * 1.66 * 1e-27
        # 87Rb mass
        kb = 1.3806 * 1e-23

        sigma_x = Gfit_params[3] * pixcal
        sigma_y = Gfit_params[4] * pixcal

        T_x = (
            (mRb / 2 / kb)
            * (np.square(self.omega_x) * np.square(sigma_x))
            / (1 + np.square(self.omega_x) * np.square(TOF))
        )
        T_y = (
            (mRb / 2 / kb)
            * (np.square(self.omega_y) * np.square(sigma_y))
            / (1 + np.square(self.omega_y) * np.square(TOF))
        )

        T = (
            2 * np.square(tau_x) / (1 + 3 * np.square(tau_x)) * T_x
            + (1 + np.square(tau_y)) / (1 + 3 * np.square(tau_y)) * T_y
        )
        T_nK = T * 1e9

        return T_nK
