import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Function to read and transpose data
def read_and_transpose_data(excel_url, sheet_name, new_columns, selected_countries):
    """
    Read and transpose data from an Excel file.

    Parameters:
    - excel_url: URL of the Excel file
    - sheet_name: Name of the sheet in the Excel file
    - new_columns: Columns to select from the data
    - selected_countries: Countries to include in the analysis

    Returns:
    - Dataframe with selected data
    - Transposed dataframe
    """
    data = pd.read_excel(excel_url, sheet_name=sheet_name, skiprows=3)
    data = data[new_columns]
    data.set_index('Country Name', inplace=True)
    data = data.loc[selected_countries]

    # Check for NaN values and replace them with 0
    data = data.replace([np.inf, -np.inf], np.nan).fillna(0)

    return data, data.T

# Excel URLs for different indicators
excel_urls = {
    'urban_population': 'https://api.worldbank.org/v2/en/indicator/SP.URB.GROW?downloadformat=excel',
    'electricity_production': 'https://api.worldbank.org/v2/en/indicator/EG.ELC.FOSL.ZS?downloadformat=excel',
    'agriculture_value_added': 'https://api.worldbank.org/v2/en/indicator/NV.AGR.TOTL.ZS?downloadformat=excel',
    'co2_emissions': 'https://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=excel',
    'forest_area': 'https://api.worldbank.org/v2/en/indicator/AG.LND.FRST.ZS?downloadformat=excel',
    'gdp_growth': 'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=excel',
}

# Common parameters
sheet_name = 'Data'
new_cols = ['Country Name', '2000', '2003', '2006', '2009', '2012', '2015']
selected_countries = ['United States', 'United Kingdom', 'Germany', 'Nigeria', 'China', 'Brazil', 'Australia']

# Read and transpose data for different indicators
data_urban, urban_transpose = read_and_transpose_data(excel_urls['urban_population'], sheet_name, new_cols, selected_countries)
data_electricity, electricity_transpose = read_and_transpose_data(excel_urls['electricity_production'], sheet_name, new_cols, selected_countries)
data_agriculture, agriculture_transpose = read_and_transpose_data(excel_urls['agriculture_value_added'], sheet_name, new_cols, selected_countries)
data_co2, co2_transpose = read_and_transpose_data(excel_urls['co2_emissions'], sheet_name, new_cols, selected_countries)
data_forest, forest_transpose = read_and_transpose_data(excel_urls['forest_area'], sheet_name, new_cols, selected_countries)
data_gdp, gdp_transpose = read_and_transpose_data(excel_urls['gdp_growth'], sheet_name, new_cols, selected_countries)

# Print dataframes
#print(data_urban)
#print(urban_transpose)
#print(data_electricity)
#print(electricity_transpose)
#print(data_agriculture)
#print(agriculture_transpose)
#print(data_co2)
##print(co2_transpose)
#print(data_forest)
#print(forest_transpose)
#print(data_gdp)
#print(gdp_transpose)

# Descriptive statistics
gdp_statistics = gdp_transpose.describe()
print(gdp_statistics)

forest_statistics = forest_transpose.describe()
print(forest_statistics)

# Function to print descriptive statistics
def print_descriptive_statistics(y_data, legends):
    for i in range(len(y_data)):
        print(f"Statistics for {legends[i]}:")
        print(y_data[i].describe())
        print("\n")
        
# Function to plot multiple lines
def plot_multiple_lines(x_data, y_data, x_label, y_label, title, legends, line_colors):
    """
    Plot multiple lines on the same graph.

    Parameters:
    - x_data: Data for the x-axis
    - y_data: Data for the y-axis
    - x_label: Label for the x-axis
    - y_label: Label for the y-axis
    - title: Title of the plot
    - legends: Legend labels for each line
    - line_colors: Colors for each line
    """
    plt.figure(figsize=(10, 8), dpi=200)
    plt.title(title, fontsize=20, fontweight='bold')
    for i in range(len(y_data)):
        plt.plot(x_data, y_data[i], label=legends[i], color=line_colors[i])
    plt.xlabel(x_label, fontsize=20, fontweight='bold')
    plt.ylabel(y_label, fontsize=20, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.02, 1))
    plt.show()
    print_descriptive_statistics(y_data, legends)

# Plot multiple lines for electricity production
x_data_electricity = electricity_transpose.index
y_data_electricity = [electricity_transpose['United States'], electricity_transpose['United Kingdom'],
                      electricity_transpose['Germany'], electricity_transpose['Nigeria'],
                      electricity_transpose['China'], electricity_transpose['Brazil'],
                      electricity_transpose['Australia']]
x_label_electricity = 'Year'
y_label_electricity = '% electricity production'
legends_electricity = ['USA', 'UK', 'Germany', 'Nigeria', 'China', 'Brazil', 'Australia']
line_colors_electricity = ['cyan', 'orange', 'pink', 'brown', 'gray', 'lime', 'indigo']
title_electricity = 'Electricity production from oil, gas and coal sources (% of total)'

plot_multiple_lines(x_data_electricity, y_data_electricity, x_label_electricity, y_label_electricity,
                    title_electricity, legends_electricity, line_colors_electricity)

# Plot multiple lines for CO2 emissions
x_data_co2 = co2_transpose.index
y_data_co2 = [co2_transpose['United States'], co2_transpose['United Kingdom'],
              co2_transpose['Germany'], co2_transpose['Nigeria'],
              co2_transpose['China'], co2_transpose['Brazil'],
              co2_transpose['Australia']]
x_label_co2 = 'Year'
y_label_co2 = 'metric tons'
legends_co2 = ['USA', 'UK', 'Germany', 'Nigeria', 'China', 'Brazil', 'Australia']
line_colors_co2 = ['cyan', 'orange', 'pink', 'brown', 'gray', 'lime', 'indigo']
title_co2 = 'CO2 emissions (metric tons per capita)'

plot_multiple_lines(x_data_co2, y_data_co2, x_label_co2, y_label_co2, title_co2, legends_co2, line_colors_co2)

# Function to plot grouped bar charts
def plot_grouped_bars(labels_array, bar_width, y_data, y_label, legends, title):
    """
    Plot grouped bar charts.

    Parameters:
    - labels_array: Labels for the x-axis
    - bar_width: Width of each bar
    - y_data: Data for the y-axis
    - y_label: Label for the y-axis
    - legends: Legend labels for each group
    - title: Title of the plot
    """
    x = np.arange(len(labels_array))
    fig, ax = plt.subplots(figsize=(12, 10), dpi=200)

    for i, year_data in enumerate(y_data):
        plt.bar(x + i * bar_width, year_data, width=bar_width, label=legends[i])

    plt.title(title, fontsize=20, fontweight='bold')
    plt.ylabel(y_label, fontsize=20, fontweight='bold')
    plt.xlabel(None)
    plt.xticks(x + (len(y_data) - 1) * bar_width / 2, labels_array)

    plt.legend()
    ax.tick_params(bottom=False, left=True)

    plt.show()
    print_descriptive_statistics(y_data, legends)

# Plot grouped bar charts for Urban population growth
labels_array_urban = selected_countries
bar_width_urban = 0.2
y_data_urban = [data_urban['2006'], data_urban['2009'],
                data_urban['2012'], data_urban['2015']]
y_label_urban = 'Urban growth'
legends_urban = ['Year 2006', 'Year 2009', 'Year 2012', 'Year 2015']
title_urban = 'Urban population growth (annual %)'

plot_grouped_bars(labels_array_urban, bar_width_urban, y_data_urban, y_label_urban, legends_urban, title_urban)

# Plot grouped bar charts for Agriculture value added (% of GDP)
labels_array_agriculture = selected_countries
bar_width_agriculture = 0.2
y_data_agriculture = [data_agriculture['2006'], data_agriculture['2009'],
                      data_agriculture['2012'], data_agriculture['2015']]
y_label_agriculture = '% of GDP'
legends_agriculture = ['Year 2006', 'Year 2009', 'Year 2015', 'Year 2017']
title_agriculture = 'Agriculture, forestry, and fishing, value added (% of GDP)'

plot_grouped_bars(labels_array_agriculture, bar_width_agriculture, y_data_agriculture, y_label_agriculture,
                  legends_agriculture, title_agriculture)

# Function to calculate correlation and p-values
def calculate_correlation_pvalues(data_x, data_y):
    corr_df = pd.DataFrame(columns=['r', 'p'])
    for col in data_y:
        if pd.api.types.is_numeric_dtype(data_y[col]) and not '':
            r, p = stats.pearsonr(data_x, data_y[col])
            corr_df.loc[col] = [round(r, 3), round(p, 3)]
    return corr_df

# Calculate correlation for GDP Annual Growth in China
data_x_china = gdp_transpose['China']
data_y_china = pd.DataFrame({
    'Urban pop. growth': urban_transpose['China'],
    'Electricity production': electricity_transpose['China'],
    'Agric. forestry and Fisheries': agriculture_transpose['China'],
    'CO2 Emissions': co2_transpose['China'],
    'Forest Area': forest_transpose['China'],
    'GDP Annual Growth': gdp_transpose['China']
})

# Remove NaN values
data_y_china = data_y_china.replace([np.inf, -np.inf], np.nan).fillna(0)

gdp_annual_growth_china = calculate_correlation_pvalues(data_x_china, data_y_china)
print(gdp_annual_growth_china)

# Calculate correlation for Forest Area in the UK
data_x_uk = forest_transpose['United Kingdom']
data_y_uk = pd.DataFrame({
    'Urban pop. growth': urban_transpose['United Kingdom'],
    'Electricity production': electricity_transpose['United Kingdom'],
    'Agric. forestry and Fisheries': agriculture_transpose['United Kingdom'],
    'CO2 Emissions': co2_transpose['United Kingdom'],
    'Forest Area': forest_transpose['United Kingdom'],
    'GDP Annual Growth': gdp_transpose['United Kingdom']
})

# Remove NaN values
data_y_uk = data_y_uk.replace([np.inf, -np.inf], np.nan).fillna(0)

forest_area_uk = calculate_correlation_pvalues(data_x_uk, data_y_uk)
print(forest_area_uk)

# Function to create correlation heatmaps
def create_correlation_heatmap(data, corr, title):
    plt.figure(figsize=(8, 8), dpi=200)
    plt.imshow(corr, cmap='coolwarm', interpolation='none')
    plt.colorbar()

    plt.xticks(range(len(data.columns)), data.columns, rotation=90, fontsize=15)
    plt.yticks(range(len(data.columns)), data.columns, rotation=0, fontsize=15)

    plt.title(title, fontsize=20, fontweight='bold')

    labels = corr.values
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            plt.text(j, i, '{:.2f}'.format(labels[i, j]), ha="center", va="center", color="white")

    plt.show()
    return

# Create correlation heatmap for China
corr_china = data_y_china.corr()
print(corr_china)

data_china = data_y_china
corr_china = corr_china
title_china = 'China'
create_correlation_heatmap(data_china, corr_china, title_china)

# Create correlation heatmap for the United Kingdom
corr_uk = data_y_uk.corr()
print(corr_uk)

data_uk = data_y_uk
corr_uk = corr_uk
title_uk = 'United Kingdom'
create_correlation_heatmap(data_uk, corr_uk, title_uk)
