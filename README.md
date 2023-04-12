# How's My Driving?
An OBD-II Trip Analysis Dashboard
<br>
<img src="https://user-images.githubusercontent.com/20276256/231508053-89862e6f-62df-41a5-aae4-5847ff1bd681.png" width="1000" />

## FAQ
### What is OBD-II?
OBD-II (On-Board Diagnostics) is a standard protocol used in modern vehicles to communicate with diagnostic equipment. This protocol provides real-time information on a vehicle's health and performance. OBD-II data can be used to analyze trips and driver behavior to improve driving efficiency, safety, and overall performance.

### How do I collect my own data?
To collect your own data, you will need an ELM327 Scanner (OBD-II port scanner). This allows you to read and log the real-time information from your vehicle's sensors. Once the trip is complete, export the logged data as CSV and upload it on the home page. It is recommended that you use the setup mentioned below for best results.

For best results follow this tutorial: [Collect Automotive Data](https://www.youtube.com/watch?v=GSSOe9I7roo)
<br>
Scanner: [ELM 327 Bluetooth Scanner](https://a.co/d/9YJaLyI)
<br>
Logger App: [Car Scanner ELM OBD2](https://www.carscanner.info/)

### What kind of analysis can I expect?
1. Speed analysis: OBD-II data can be used to track the speed of the vehicle during a trip. This data can be used to analyze the driver's speed behavior, including speeding, rapid acceleration, and hard braking.
2. Fuel efficiency analysis: OBD-II data can provide information on fuel consumption, including fuel economy, fuel level, and fuel consumption rate. This data can help you optimize routes and reduce fuel costs.
3. Trip analysis: OBD-II data can provide information on the length of a trip, average speed, distance traveled, and time spent idling.
4. Driver behavior analysis: OBD-II data can provide information on driver behavior, including aggressive driving, hard braking, rapid acceleration, and excessive idling.

## Installation
1. Clone the repository
```bash
git clone https://github.com/Ninkuk/howsmydriving.git
cd howsmydriving
```

2. Create and activate a [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) environment from the environment.yml file.
```bash
conda env create -f environment.yml

# or use environment.txt
conda create --name <env> --file environment.txt

conda activate howsmydriving
```

3. Run the application
```bash
flask run
# or
flask --debug run
```
The application should now be running on http://localhost:5000.
