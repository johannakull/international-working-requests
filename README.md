# International Working Request Calculator

This is a personal Python project that helps manage international working periods in accordance with company policies for international working requests.

### Features
- **Calculate the submission deadline** for an international working request based on the desired start date.
- **Check eligibility** of a proposed international working period in relation to existing periods.
- **Record new international working periods** and store them in a CSV file.

### How to Run the Project
1. Clone the repository to your local machine.
2. Create an empty CSV file called "international_working_days.csv" in the root of the repository.
3. Adjust the constants in the constants.py file according to your company’s international working request policies (e.g., minimum notice days, lookback period).
4. Make sure you have the required dependencies (`dateutil` library) installed:
   ```bash
   pip install python-dateutil
5. Run the program by executing `main.py`:
   ```bash
   python main.py
