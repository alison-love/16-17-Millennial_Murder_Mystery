# Millennial Murder Mystery

## Project Overview

The Consumer Data Visualization application is a data-driven web platform built with Flask and Plotly. It enables users to interactively visualize consumer behavior across various demographic groups and categories over time. 

## Data Description

The dataset used in this application contains consumer statistics collected by the Bureau of Labor Statistics over the years 2019-2022. Each record in the dataset consists of the following fields:

- `id`: Unique identifier for the record.
- `year`: The year the data was collected.
- `item`: The item or metric being measured (e.g., "Share", "Mean", "SE").
- `all_consumer_units`: The aggregated measure for all consumer units.
- `gen_z`, `millennials`, `gen_x`, `baby_boomers`, `silent_generation`: Measures for different generational groups.
- `main_category`: The broad category of the item (e.g., "Consumer unit characteristics", "Sources of income and personal taxes").
- `subcategory`: A more specific category of the item.

## Features

- **Filter Selection**: Users can filter the data by generation, year, main category, subcategory, and items.
- **Chart Visualization**: The application displays the data in various chart forms such as line, bar, scatter, and pie charts.
- **Responsive Design**: The platform is designed to be responsive and user-friendly across different devices and screen sizes.

## Getting Started

To get started with the Consumer Data Visualization app:

1. Ensure you have Python and PostgreSQL installed on your system.
2. Clone this repository to your local machine.
3. Install the necessary Python packages using `pip install -r requirements.txt`.
4. Set up your PostgreSQL database and import the consumer data.
5. Update the `SQLALCHEMY_DATABASE_URI` in the Flask app configuration with your database details.
6. Run the Flask app using `python app.py`.

## Usage

Navigate to the hosted application URL and use the dropdown menus to filter data based on your interests. Select a chart type to visualize the data. The charts are interactive, allowing for a deeper dive into the data points.

## Folder Structure

The project structure is organized as follows:

Millennial_Murder_Mystery/ <br>
|-- app.py <br>
|-- Data-Cleaning_SQL-Upload.ipynb <br>
|-- excel files/ <br>
|-- static/ <br>
|-- README.md <br>
|-- ... <br>

## Dependencies

The application relies on the following dependencies:

- Flask
- SQLAlchemy
- pandas
- plotly
- flask_cors

These dependencies can be installed using `pip` as mentioned in the installation instructions.

## Data Sourcing and Ethics
The consumer data used in this project was sourced responsibly from the Bureau of Labor Statistics, ensuring the data's integrity and the privacy of individuals. We are dedicated to ethical data practices by only using aggregated and anonymized datasets, thus mitigating any risk of personal data exposure. Our analysis does not discriminate against any individual or group, and we strive to present the information in a manner that is both informative and respectful.
[
](https://www.bls.gov/cex/tables/calendar-year/mean-item-share-average-standard-error.htm)

## Contributing

Contributions to enhance the application are welcome. Please fork the repository, create a feature branch, and submit a pull request for review.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Contact

For any further queries or suggestions, please contact the repository owner.

Project Link: https://github.com/alison-love/Millennial_Murder_Mystery.git
