### How to Download and Use Xlarcys Toolkit on Kali Linux

1. **Open Kali Linux**: Boot your system and open the Kali Linux terminal.

2. **Install Git**: If Git is not installed, you can install it with the following commands:
   ```bash
   sudo apt-get update
   sudo apt-get install git
   ```

3. **Clone the Repository**: To clone the Xlarcys Toolkit GitHub repository, type the following command in the terminal:
   ```bash
   git clone https://github.com/username/repo-name.git
   ```
   (Replace `username` and `repo-name` with your own repository information.)

4. **Install Requirements**: To install Python and the required libraries, use these commands:
   ```bash
   sudo apt-get install python3
   pip3 install requests beautifulsoup4
   ```

5. **Run the Toolkit**:
   - Navigate to the cloned directory:
   ```bash
   cd repo-name
   ```
   - To run the main script:
   ```bash
   python3 main.py
   ```

6. **Using the Tool**:
   - Choose scan or shell upload options from the menu.
   - Enter the relevant URLs and proceed with the actions.

7. **Developer Note**: Always remember to use this tool ethically. Make sure to obtain permission before conducting tests.

These steps explain how to install and use the Xlarcys Toolkit on Kali Linux. If you encounter any issues, refer to the documentation or the GitHub page.
