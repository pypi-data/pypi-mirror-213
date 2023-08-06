from pathlib import Path
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import torch
import random

from mir_ml_utils.utils.file_utils import load_list_from_csv
from mir_ml_utils.utils.exceptions import SizeMismatchException


def set_seed(seed: int) -> None:
    """Set the seed for various
    underlying components

    Parameters
    ----------
    seed: The seed to use

    Returns
    -------

    """

    # Disable cudnn to maximize reproducibility
    torch.cuda.cudnn_enabled = False
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    #torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def _add_plot(n_epochs: int, data_path: Path, label: str,
              step_length: int = 100, use_mean_smoothing: bool = True):

    data = load_list_from_csv(filename=data_path)
    data_avg = np.empty(n_epochs)

    if use_mean_smoothing:
        for t in range(n_epochs):
            data_avg[t] = np.mean(data[max(0, t - step_length): (t + 1)])

        plt.plot(data_avg, label=label)
    else:
        plt.plot(data, label=label)


def plot_generalization_error_from_path(train_path: Path,
                                        val_path: Path,
                                        use_mean_smoothing: bool = True,
                                        step_length: int = 1,
                                        save_file: Path = None,
                                        title: str = "Generalization error", show_before_save: bool = False):

    train_data = load_list_from_csv(filename=train_path)
    val_data = load_list_from_csv(filename=val_path)

    if len(train_data) != len(val_data):
        raise SizeMismatchException(size1=len(train_data), size2=len(val_data))

    if use_mean_smoothing:

        train_data_avg = np.empty(len(train_data))
        val_data_avg = np.empty(len(train_data))
        for t in range(len(train_data)):  # avg_rewards.shape[0]):
            train_data_avg[t] = np.mean(train_data[max(0, t - step_length): (t + 1)])
            val_data_avg[t] = np.mean(val_data[max(0, t - step_length): (t + 1)])

        data_avg = val_data_avg - train_data_avg
        plt.plot(data_avg, label="Generalization error")
    else:

        data = np.array(val_data) - np.array(train_data)
        plt.plot(data, label="Generalization error")

    plt.legend(loc='best')
    plt.grid(True)
    plt.title(title)

    if save_file is not None:

        if show_before_save:
            plt.show()

        plt.savefig(str(save_file))

        # need to close the figure
        # otherwise it may be overriden
        plt.close()
    else:
        plt.show()


def plot_curve(curve: List[float],
               use_mean_smoothing: bool = True,
               step_length: int = 1,
               save_file: Path = None,
               title: str = "Generalization error",
               show_before_save: bool = False,
               label: str = ""):

    data_avg = np.empty(len(curve))

    if use_mean_smoothing:
        for t in range(len(curve)):
            data_avg[t] = np.mean(curve[max(0, t - step_length): (t + 1)])

        plt.plot(data_avg, label=label)
    else:
        plt.plot(curve, label=label)

    plt.legend(loc='best')
    plt.grid(True)
    plt.title(title)

    if save_file is not None:

        if show_before_save:
            plt.show()

        plt.savefig(str(save_file))

        # need to close the figure
        # otherwise it may be overriden
        plt.close()
    else:
        plt.show()



def plot_generalization_error(train_error: List[float],
                              val_error: List[float],
                              use_mean_smoothing: bool = True,
                              step_length: int = 1,
                              save_file: Path = None,
                              title: str = "Generalization error", show_before_save: bool = False):

    if len(train_error) != len(val_error):
        raise SizeMismatchException(size1=len(train_error), size2=len(val_error))

    if use_mean_smoothing:

        train_data_avg = np.empty(len(train_error))
        val_data_avg = np.empty(len(train_error))
        for t in range(len(train_error)):
            train_data_avg[t] = np.mean(train_error[max(0, t - step_length): (t + 1)])
            val_data_avg[t] = np.mean(val_error[max(0, t - step_length): (t + 1)])

        data_avg = val_data_avg - train_data_avg
        plt.plot(data_avg, label="Generalization error")
    else:

        data = np.array(val_error) - np.array(train_error)
        plt.plot(data, label="Generalization error")

    plt.legend(loc='best')
    plt.grid(True)
    plt.title(title)

    if save_file is not None:

        if show_before_save:
            plt.show()

        plt.savefig(str(save_file))

        # need to close the figure
        # otherwise it may be overriden
        plt.close()
    else:
        plt.show()


def plot_avg_train_validate_loss(n_epochs, train_loss: Path, step_length: int =100,
                                 validate_loss: Path=None, use_mean_smoothing: bool = True,
                                 save_file: Path = None,
                                 title: str = None, show_before_save: bool = False):
    # load training loss and accuracy

    if train_loss is not None:
        _add_plot(n_epochs=n_epochs, data_path=train_loss,
                  step_length=step_length, label="Train loss",
                  use_mean_smoothing=use_mean_smoothing)

    if validate_loss is not None:
        _add_plot(n_epochs=n_epochs, data_path=validate_loss, step_length=step_length,
                  label="Validate loss", use_mean_smoothing=use_mean_smoothing)

    plt.xlabel("Epoch" if use_mean_smoothing else "Iteration")
    plt.ylabel("Loss")
    if validate_loss is not None and train_loss is not None:

        if title is None:
            plt.title("Average train/validate loss over epochs")
        else:
            plt.title(title)
    elif train_loss is not None:

        plt.title("Average train loss over epochs")

        if title is not None:
            plt.title(title)

    elif validate_loss is not None:
        plt.title("Average validate loss over epochs")

        if title is not None:
            plt.title(title)
    else:
        raise ValueError("No file path is specified")

    plt.legend(loc='best')
    plt.grid(True)

    if save_file is not None:

        if show_before_save:
            plt.show()

        plt.savefig(str(save_file))

        # need to close the figure
        # otherwise it may be overriden
        plt.close()
    else:
        plt.show()


def plot_avg_train_validate_accuracy(n_epochs: int, train_accuracy: Path,
                                     step_length: int = 100,
                                     validate_accuracy: Path=None,
                                     use_mean_smoothing: bool = True,
                                     save_file: Path = None,
                                     title: str = None,
                                     show_before_save: bool = False):

    if train_accuracy is not None:
        _add_plot(n_epochs=n_epochs, data_path=train_accuracy,
                  step_length=step_length, label="Train accuracy",
                  use_mean_smoothing=use_mean_smoothing)

    if validate_accuracy is not None:
        _add_plot(n_epochs=n_epochs, data_path=validate_accuracy,
                  step_length=step_length, label="Validate accuracy",
                  use_mean_smoothing=use_mean_smoothing)

    plt.xlabel("Epoch" if use_mean_smoothing else "Iteration")
    plt.ylabel("Accuracy")
    if validate_accuracy is not None:
        plt.title("Average train/validate accuracy over epochs")
    else:
        plt.title("Average train accuracy over epochs")

    if title is not None:
        plt.title(title)

    plt.legend(loc='best')
    plt.grid(True)

    if save_file is not None:

        if show_before_save:
            plt.show()

        plt.savefig(str(save_file))

        # need to close the figure
        # otherwise it may be overriden
        plt.close()
    else:
        plt.show()


def plot_avg_test_accuracy(n_epochs: int, test_accuracy: Path,
                           step_length: int = 100,
                           use_mean_smoothing: bool = True):
    _add_plot(n_epochs=n_epochs, data_path=test_accuracy,
              step_length=step_length, label="Test accuracy",
              use_mean_smoothing=use_mean_smoothing)

    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Average test accuracy over epochs")
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()


