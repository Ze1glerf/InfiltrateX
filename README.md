### How to Download and Use Xlarcys Toolkit on Kali Linux

1. **Open Kali Linux**: Boot your system and open the Kali Linux terminal.

2. **Install Git**: If Git is not installed, you can install it with the following commands:
   ```bash
   sudo apt-get update
   sudo apt-get install git
   ```

3. **Clone the Repository**: To clone the Xlarcys Toolkit GitHub repository, type the following command in the terminal:
   ```bash
   git clone https://github.com/Xlarcys01/InfiltrateX.git
   ```

4. **Install Requirements**: To install Python and the required libraries, use these commands:
   ```bash
   sudo apt-get install python3
   pip3 install -r requirements.txt
   ```

5. **Run the Toolkit**:
   - Navigate to the cloned directory:
   ```bash
   cd InfiltrateX  # Ensure the correct path
   ```
   - To run the main script:
   ```bash
   sudo python3 infiltratex.py
   ```

6. **Using the Tool**:
   - Choose scan or shell upload options from the menu.
   - Enter the relevant URLs and proceed with the actions.

7. **Developer Note**: Always remember to use this tool ethically. Make sure to obtain permission before conducting tests.
