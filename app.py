import streamlit as st
import requests
import plotly.io as pio

def get_info(req, s):
    response = requests.get(req)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        st.write(s)  # ,
        st.dataframe(data)
    else:
        st.error("Error querying data")

def get_text_info(req, s):
    response = requests.get(req)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        st.write(s)  # ,
        st.text(data)
    else:
        st.error("Error querying data")

def get_graph(req, s):
    response = requests.get(req)
    if response.status_code == 200:
        fig = pio.from_json(response.json())
        st.write(s)  # ,
        st.plotly_chart(fig)
    else:
        st.error("Error graph data")


# FastAPI endpoint
API_URL = "http://127.0.0.1:8000"

st.title("Banana App")

# Query section
st.header("Banana Dataset")
st.image("banana_and_minion.jpg")
st.markdown("""
This comprehensive banana dataset captures important information about banana samples from different regions and varieties. The key attributes are:

**sample_id**: A unique identifier assigned to each banana sample in the dataset. This allows the samples to be tracked and referenced uniquely.

**variety**: The cultivar or breed of banana, such as Cavendish, Red Dacca, or Lady Finger. Knowing the specific banana variety provides context about the sample"s physical characteristics and growing conditions.

**region**: The geographic origin of the banana, such as Ecuador, Philippines, or Costa Rica. The region can influence factors like climate, soil, and growing practices that impact the banana"s qualities.

**quality_score**: A numerical score, likely on a scale of 1-4 that rates the overall quality of the banana sample. This could encompass factors like appearance, texture, and lack of defects.

**quality_category**: A text label that categorizes the quality score into broader groupings like "Excellent" etc
This provides an easier-to-understand quality assessment.

**ripeness_index**: A numerical index representing the ripeness level of the banana, potentially ranging from 1 (green/unripe) to 10 (overripe). This quantifies the maturity of the fruit.

**ripeness_category**: A text label like "Green", "Yellow", "Ripe", or "Overripe" that corresponds to the ripeness index. This gives a clear, qualitative ripeness classification.

**sugar_content_brix**: The sugar content of the banana measured in degrees Brix. This is a common way to assess the sweetness and quality of the fruit.

**firmness_kgf**: The firmness of the banana measured in kilograms-force. This indicates the texture and maturity of the sample.

**length_cm**: The physical length of the banana in centimeters. This size metric can vary by variety and growing conditions.

**weight_g**: Weight of banana in grams

**harvest_date**: the day when the harvest was gathered

**tree_age_years**: tree age

**altitude_m**: The altitude of tree in metres

**rainfall_mm**: amount of precipitation in millimeters

**soil_nitrogen_ppm**: nitrogen concentration in soil in parts per million
""")

get_info(f"{API_URL}/get_df", "Our DataFrame")

st.header("Descriptive statistics for 3 numerical fields")
get_info(f"{API_URL}/mean", "Mean statistics:")
get_info(f"{API_URL}/median", "Median statistics:")
get_info(f"{API_URL}/std", "Std statistics:")

st.header("Data cleanup")
st.markdown("Let's check data types")
get_text_info(f"{API_URL}/info", "Data info:")
st.markdown("""
We can see that every Dtype are correspond expected types

Check amount of NaNs in dataset""")
get_info(f"{API_URL}/nan", "Count nans:")

st.markdown("""
There is no NaN in the dataset

Let"s look if there are some outlier in the Dataset""")

get_graph(f"{API_URL}/box1", "Plot1_quality_sc_ripness_ind")

get_info(f"{API_URL}/analys1", "check data where 'quality_score' < 1.2")
get_info(f"{API_URL}/analys2", "look at correlation:")

st.text("Despite the fact that we have a rather small value in quality_score I don't think that it is outlier because it seems similar at the rest data")
get_graph(f"{API_URL}/box2", "Plot2_firmness_kgf")
get_graph(f"{API_URL}/box3", "Plot3_sugar_length")
get_graph(f"{API_URL}/box4", "Plot4_weight_nitrogen")
get_graph(f"{API_URL}/box5", "Plot5_tree_age_years")
get_graph(f"{API_URL}/box6", "Plot6_altitude_rainfall")

st.text("Looking at the rest boxplots we can see that they don't have any outliers")
st.header("Plots")
st.text("The histogram below show the amaount of bananas at every length from 9 sm to 30 sm, and we do not see any dependencies")

get_graph(f"{API_URL}/hist", "")
st.text("Below I looked at the correletion and decided to do two scatter plots with quality_score and ripeness_index, quality_score and sugar_content_brix")
get_info(f"{API_URL}/data3", "look at correlation:")

get_graph(f"{API_URL}/scatter", "Plot7")
get_graph(f"{API_URL}/scatter2", "Plot8")
get_graph(f"{API_URL}/scatter3", "Plot9")
st.text("Also i decided to split them into categories and we can se that they are depended")
st.text("Here I've done a bar plot wich show how many bananas are in each kind of them and we can see that they are quite similar")
get_graph(f"{API_URL}/diff_plot", "Plot10")
st.text("Here I've done a bar plot wich show how many bananas are in each country and we can see that they are quite similar")
get_graph(f"{API_URL}/diff_plot2", "Plot11")
st.text("Below we can see two graphs that show us the comparison of the amount of bananas each category wich separated by kinds of banana or territory")
get_graph(f"{API_URL}/boxx2", "Plot12")
st.text("In all regions the amount of unripe and premium bananas are small however the amount of processing and godd bananas are much bigger, also we can see that amount of processing bananas in Ecuador are much bigger than good number bananas")
get_graph(f"{API_URL}/boxx3", "Plot12")
st.text("Here also in all kinds of bananas the amount of unripe and premium bananas are small however the amount of processing and good bananas are much bigger")

st.header("Data transformation")
st.text("Let's do two new columns: quality_number(quality category turned to number from 1 to 4) and sugar_g(the amount of sugar in gramms)")
get_info(f"{API_URL}/change", "Transformed data:")

st.header("Hypotesis")
st.text("What if than ripness_index and sugar_content_brix are big than quality_number is also big")
get_info(f"{API_URL}/corr1", "Corr data:")
get_graph(f"{API_URL}/hypo", "Plot14")
get_graph(f"{API_URL}/hypo2", "Plot13")
st.text("It means that sugar_content_brix and ripness index impact on quality_number as unripe bananas do not cross with Premium and cross only with processing banans and premium bananas cross only with good bananas, so we can see a quality_category smoothly grows with rise of sugar_content_brix and ripness_index")

st.header("Filter data")


#rip = st.number_input("Ripeness_index", min_value=0.0, value=2.0, step=0.01, format="%.2f")
#qua = st.number_input("Quality_score", min_value=0.0, value=0.0, step=0.01, format="%.2f")

countries = ["Brazil",
 "Colombia",
 "Costa Rica",
 "Ecuador",
 "Guatemala",
 "Honduras",
 "India",
 "Philippines"]

choice_c = st.selectbox("Choose country", countries)
types = ["Blue Java",
 "Burro",
 "Cavendish",
 "Fehi",
 "Lady Finger",
 "Manzano",
 "Plantain",
 "Red Dacca"]
choice_t = st.selectbox("Choose breed", types)
if st.button("Search"):
    response = requests.get(f"{API_URL}/filter", params={"country": choice_c, "type": choice_t})
    if response.status_code == 200:
        data = response.json()
        #print(data)
        st.text("Results:")
        st.dataframe(data)
    else:
        st.error("Error querying data")

# Add section
st.header("Add New Banana")
clas = ["Unripe",
 "Processing",
 "Good",
 "Premium"]

choice_cc = st.selectbox("Choose a country", countries)
choice_tt = st.selectbox("Choose a breed", types)
choice_cl = st.selectbox("Choose a banana class", clas)
#qua = st.number_input("Quality_score", min_value=0.0, value=0.0, step=0.01, format="%.2f")
rip = st.number_input("Ripeness_index", min_value=0.0, value=0.0, step=0.01, format="%.2f")

if st.button("Add Entry"):
    data = {"country": choice_cc, "type": choice_tt, "quality_category": choice_cl, "ripeness_index": rip}
    response = requests.post(f"{API_URL}/add", json=data)
    if response.status_code == 200:
        st.success("Entry added successfully!")
        data = response.json()
        st.dataframe(data)
    else:
        st.error("Error adding entry")