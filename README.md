# Longlist_Generator
 # CV Filtration App

This application filters CVs based on given criteria using OpenAI's API. Follow the steps below to set up and run the application.

## Setup

1. **Clone the Repository**

    Clone the repository to your local machine and navigate to the project directory.

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Install Required Packages**

    Install the required packages using `pip`. Ensure you have the necessary packages (`openai`, `python-docx`, `PyPDF2`). You can install them individually:

    ```bash
    pip install openai python-docx PyPDF2
    ```

3. **Configure Your OpenAI API Key**

    Create a `config.py` file in the project directory and add your OpenAI API key. This file will be ignored by Git to keep your key secure.

    **config.py:**

    ```python
    OPENAI_API_KEY = 'your_openai_api_key_here'
    ```

4. **Running the Application**

    - **Windows**: Double-click the `run_script.bat` file to run the application.


## .gitignore

Make sure your `.gitignore` file includes `config.py` to keep it secure:

**.gitignore:**

```gitignore
config.py

**Notes**

- Ensure your Python installation is added to the system's PATH.
- This setup assumes you have Python and `pip` installed on your system.
- For security reasons, never share your `config.py` file or API key publicly.

## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


