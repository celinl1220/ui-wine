# How to Run the Python Flask Application

This README provides instructions on how to run the Python Flask application `app.py`.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python 3:** Flask requires Python 3. You can check if you have Python 3 installed by opening your terminal or command prompt and running:
    ```bash
    python3 --version
    ```
    If Python 3 is not installed, you can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

* **pip:** pip is the package installer for Python. It usually comes bundled with Python 3. You can check if you have pip installed by running:
    ```bash
    pip3 --version
    ```
    If pip is not installed or needs an upgrade, you can find instructions on how to install it here: [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)

* **Flask:** Flask is the micro web framework written in Python that this application uses. You need to install it using pip:
    ```bash
    pip3 install Flask
    ```

## Running the Application (Simple Method)

1.  **Run the `app.py` script:** Execute the `app.py` file using the Python 3 interpreter:
    ```bash
    python3 app.py
    ```

    You should see output similar to this:

    ```
     * Serving Flask app 'app'
     * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on [http://127.0.0.1:5001](http://127.0.0.1:5001) (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: xxx-xxx-xxx
    ```

2.  **Access the application in your web browser:** Open your web browser and go to the address indicated in the output (usually `http://127.0.0.1:5001/`).

3.  **Stop the development server:** To stop the Flask development server, go back to your terminal or command prompt and press `Ctrl + C`.

## Alternative Method (Using `flask run`)

1.  **Set the Flask application environment variable:**
    * **Linux and macOS:**
        ```bash
        export FLASK_APP=app.py
        ```
    * **Windows (using Command Prompt):**
        ```bash
        set FLASK_APP=app.py
        ```
    * **Windows (using PowerShell):**
        ```powershell
        $env:FLASK_APP = "app.py"
        ```

2.  **Run the Flask development server:**
    ```bash
    flask run
    ```

## Additional Notes

* **Debug Mode:** For development, you can enable debug mode using the `FLASK_DEBUG` environment variable (set it to `1`) or often directly in your `app.py` when calling `app.run(debug=True)`. **Disable debug mode in production.**

* **Custom Host and Port:** You can specify a host and port using `app.run(host='0.0.0.0', port=8000)` in your `app.py` or using the `--host` and `--port` options with `flask run`.
