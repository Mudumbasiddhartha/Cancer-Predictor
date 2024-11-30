# Cancer Predictor

This project aims to predict cancer using machine learning algorithms. The repository contains the necessary code and data to train and test the model.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Contributing](#contributing)


## Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mudumbasiddhartha/Cancer-Predictor.git
   cd Cancer-Predictor
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the Cancer Predictor, follow these steps:

1. **Prepare the data**:
   - Ensure that the `db.sqlite3` file is in the root directory of the project.

2. **Run the application**:
   ```bash
   python manage.py runserver
   ```

3. **Access the application**:
   - Open your web browser and go to `http://127.0.0.1:8000/` to access the Cancer Predictor application.

## How It Works

### Django Framework

The project is built using the Django framework, which is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Django handles the backend operations, including database management, URL routing, and template rendering.

### Machine Learning Model

The machine learning model used in this project is a Decision Tree Classifier that predicts the likelihood of cancer based on input features. The model is trained using a dataset containing various attributes related to cancer diagnosis. The key steps involved in the machine learning process are:

1. **Data Preprocessing**: Cleaning and preparing the data for training.
2. **Model Training**: Using the Decision Tree algorithm to train the model.
3. **Model Evaluation**: Assessing the model's performance using metrics like accuracy, precision, recall, and F1-score.
4. **Prediction**: Using the trained model to make predictions on new data.

The `classifier` directory contains the scripts for training and predicting using the machine learning model.

### ROC Curve and Results

The application also generates a Receiver Operating Characteristic (ROC) curve to visualize the performance of the classifier. The ROC curve is displayed on the web page along with the prediction results, indicating whether the cell is affected or not.

## Project Structure

The project structure is as follows:

```
Cancer-Predictor/
├── cancer_prj/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
├── classifier/
│   ├── __init__.py
│   ├── model.py
│   ├── train.py
│   ├── predict.py
│   ├── templates/
│   │   └── classifier/
│   │       └── home.html
├── db.sqlite3
├── manage.py

```

- `cancer_prj/`: Contains the Django project files.
- `classifier/`: Contains the machine learning model files and templates.
- `db.sqlite3`: The SQLite database file.
- `manage.py`: The Django management script.
- `requirements.txt`: The list of dependencies.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a pull request.

