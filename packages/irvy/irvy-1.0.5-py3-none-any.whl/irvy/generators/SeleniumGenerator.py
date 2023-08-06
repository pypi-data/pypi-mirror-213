import os
import subprocess


class SeleniumGenerator:
    def __init__(self, language):
        self.language = language

    def generate(self):
        if self.language == "csharp":
            self.create_csharp_selenium()
        elif self.language == "python":
            self.create_python_selenium_project()
            self.create_readme()
        elif self.language == "javascript":
            self.create_javascript_selenium_project()

    def create_python_selenium_project(self):
        os.system("mkdir SeleniumPython")
        os.chdir("SeleniumPython")
        os.system("mkdir tests pages utils")

        with open('requirements.txt', 'w') as f:
            f.write('selenium\n')
            f.write('pytest\n')
            f.write('pytest-xdist\n')
            f.write('webdriver_manager\n')

        with open('tests/__init__.py', 'w') as f:
            f.write('')

        # Create a test script in the tests directory
        with open('tests/test_login.py', 'w') as f:
            f.write('import pytest\n')
            f.write('from selenium import webdriver\n')
            f.write('from pages.login_page import LoginPage\n\n')
            f.write('from selenium import webdriver\n\n')
            f.write('from webdriver_manager.chrome import ChromeDriverManager\n\n')
            f.write('def test_login():\n')
            f.write('    driver = webdriver.Chrome(ChromeDriverManager().install())\n')
            f.write('    driver = webdriver.Chrome()\n')
            f.write('    login_page = LoginPage(driver)\n')
            f.write('    login_page.login("tomsmith", "SuperSecretPassword!")\n')
            f.write('    assert login_page.is_logged_in()')

        with open('pages/__init__.py', 'w') as f:
            f.write('')
        # Create a page object model in the pages directory
        with open('pages/login_page.py', 'w') as f:
            f.write('class LoginPage:\n')
            f.write('    def __init__(self, driver):\n')
            f.write('        self.driver = driver\n\n')
            f.write('    def login(self, username, password):\n')
            f.write('        # add code to login here\n')
            f.write('        pass\n\n')
            f.write('    def is_logged_in(self):\n')
            f.write('        # add code to check login status here\n')
            f.write('        return True\n')

        with open('utils/__init__.py', 'w') as f:
            f.write('')
        # Create a utility function in the utils directory
        with open('utils/helpers.py', 'w') as f:
            f.write('def helper_function():\n')
            f.write('    # add code for the helper function here\n')
            f.write('    pass\n')

    def create_csharp_selenium(self):
        # create new console application
        subprocess.run("dotnet new console -n SeleniumCsharp",
                    shell=True, check=True)

        # change directory to the new project
        os.chdir("SeleniumCsharp")

        # add Selenium.WebDriver package
        subprocess.run("dotnet add package Selenium.WebDriver",
                    shell=True, check=True)
        subprocess.run("dotnet add package NUnit",
                    shell=True, check=True)
        subprocess.run("dotnet add package NUnit3TestAdapter",
                    shell=True, check=True)
        subprocess.run("dotnet add package Microsoft.NET.Test.Sdk",
                    shell=True, check=True)
        subprocess.run("dotnet add package XunitXml.TestLogger --version 3.0.67",
                    shell=True, check=True)

        # create necessary directories
        os.makedirs("Pages", exist_ok=True)
        os.makedirs("Tests", exist_ok=True)
        os.makedirs("Utils", exist_ok=True)

        # create boilerplate files
        with open("Pages/LoginPage.cs", "w") as file:
            file.write(
                '''

    using OpenQA.Selenium;

    namespace Pages
    {
        public class LoginPage
        {
            private IWebDriver _driver;

            public LoginPage(IWebDriver driver)
            {
                _driver = driver;
            }

            public void EnterUsername(string username)
            {
                var usernameField = _driver.FindElement(By.Id("username")); // replace "username" with the actual id of the username field
                usernameField.SendKeys(username);
            }

            public void EnterPassword(string password)
            {
                var passwordField = _driver.FindElement(By.Id("password")); // replace "password" with the actual id of the password field
                passwordField.SendKeys(password);
            }

            public void ClickLoginButton()
            {
                var loginButton = _driver.FindElement(By.XPath("//*[@id='submit']")); // replace "loginButton" with the actual id of the login button
                loginButton.Click();
            }
        }
    }

                    

                    '''
            )

        with open("Tests/LoginTest.cs", "w") as file:
            file.write(
                '''
    using NUnit.Framework;
    using OpenQA.Selenium;
    using OpenQA.Selenium.Chrome;
    using Pages;
    using SeleniumCsharp.Utils; // Add this

    namespace Tests
    {
        public class LoginTest
        {
            private IWebDriver? driver;
            private LoginPage? loginPage;

            [SetUp]
            public void Setup()
            {
                driver = new ChromeDriver();
                loginPage = new LoginPage(driver);
                driver.Navigate().GoToUrl(Configuration.Url); // Use Configuration.Url
            }

            [Test]
            public void TestLogin()
            {
                loginPage.EnterUsername(Configuration.Username); // Use Configuration.Username
                loginPage.EnterPassword(Configuration.Password); // Use Configuration.Password
                loginPage.ClickLoginButton();
                // TODO: Verify successful login
            }

            [TearDown]
            public void Teardown()
            {
                driver?.Quit();
            }
        }
    }
                        '''
            )

        with open("Utils/Helper.cs", "w") as file:
            file.write("// TODO: implement helper\n")

        with open("Utils/Configuration.cs", "w") as file:
            file.write(
                '''
                    namespace SeleniumCsharp.Utils
                    {
                        public static class Configuration
                        {
                            public const string Url = "https://practicetestautomation.com/practice-test-login/";
                            public const string Username = "student";
                            public const string Password = "Password123";
                            public static readonly bool Headless = false;
                        }
                    }
                    '''
            )

            with open("Program.cs", "w") as file:
                file.write(
                    '''
    using System;
    using Tests;

    namespace SeleniumCsharp
    {
        class Program
        {
            static void testLogin(string[] args)
            {
                LoginTest loginTest = new LoginTest();
                loginTest.TestLogin();
            }
        }
    }

                                    '''
                )
                with open("readme.md", "w") as file:
                    file.write(
                        '''
    # Selenium C# Test Automation

    This is a simple C# Selenium test automation project. It uses Selenium WebDriver and NUnit for testing a sample login page.

    ## Table of Contents
    - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installing Dependencies](#installing-dependencies)
    - [Running Tests](#running-tests)
    - [Configurations](#configurations)
    - [Built With](#built-with)
    - [Acknowledgments](#acknowledgments)

    ## Getting Started

    These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

    ### Prerequisites

    What things you need to install:

    - .NET Core SDK (version 7.0 or above)
    - Chrome Browser (latest version recommended)

    ### Installing Dependencies

    Navigate to the project directory and install the necessary packages by running:

    ```bash
    dotnet restore
    dotnet build
    ```

    ## Running Tests      

    ```
    dotnet test
    ```

    To generate an XML report, use:

    ```
    dotnet test --logger:"xunit;LogFileName=test-results.xml"
    ```

    ## Configurations
    All configurations are stored in the Configuration class in the Utils namespace. This includes the URL, username, password, and headless browser option.

    ## Built With
    Selenium WebDriver
    NUnit              
                        '''
                    )

    def create_javascript_selenium_project(self):
        base_dir = os.getcwd()
        tests_dir = os.path.join(base_dir, "tests")
        pages_dir = os.path.join(base_dir, "pages")

        os.makedirs(tests_dir, exist_ok=True)
        os.makedirs(pages_dir, exist_ok=True)
        with open(os.path.join(base_dir, "config.json"), "w") as f:
            f.write('''
                {
        "selenium": {
            "browser": "chrome",
            "chromeOptions": [
                "--ignore-certificate-errors",
                "--acceptInsecureCerts",
                "start-maximized",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-logging",
                "--log-level=3",
                "--output=/dev/null",
                "--disable-in-process-stack-traces"
            ]
        },
        "testUrl": "https://practicetestautomation.com/practice-test-login/"
    }
                ''')
        # Create a package.json file
        with open(os.path.join(base_dir, "package.json"), "w") as f:
            f.write('''
    {
        "name": "javascript-selenium-boilerplate",
        "version": "1.0.0",
        "description": "",
        "type": "module",
        "main": "index.js",
        "scripts": {
            "test": "mocha ./tests/*.js --reporter xunit --reporter-options output=results.xml"
        },
        "keywords": [],
        "author": "",
        "license": "ISC",
        "devDependencies": {
            "chromedriver": "^112.0.1",
            "mocha": "^10.2.0",
            "selenium-webdriver": "^4.9.2"
        }
    }
            ''')
        # Create a sample test file
        with open(os.path.join(tests_dir, "login_test.js"), "w") as f:
            f.write("""import { Builder, By, until } from 'selenium-webdriver';
    import { Options } from 'selenium-webdriver/chrome.js';
    import LoginPage from '../pages/LoginPage.js';
    import config from '../config.json' assert { type: "json" };
    import assert from 'assert';

    describe('Login Page Tests', function() {
        this.timeout(5000); // Specify the test suite timeout
        let driver;
        let loginPage;

        before(async function() {
            const chromeOptions = new Options();
            config.selenium.chromeOptions.forEach(option => chromeOptions.addArguments(option));

            driver = await new Builder()
                .forBrowser(config.selenium.browser)
                .setChromeOptions(chromeOptions)
                .build();

            loginPage = new LoginPage(driver);
        });

        it('should open the login page', async function() {
            await loginPage.openLoginPage(config.testUrl); 
        });

        it('should login', async function() {
            await loginPage.openLoginPage(config.testUrl);
            await loginPage.login();
        });

        after(async function() {
            await driver.quit();
        });
    });
            """)

        # Create a sample page file
        with open(os.path.join(pages_dir, "LoginPage.js"), "w") as f:
            f.write("""
    import { By } from 'selenium-webdriver';

    class LoginPage {
    constructor(driver) {
        this.driver = driver;
        this.locators = {
        user: By.id('username'),
        password: By.id('password'),
        loginButton: By.id('submit'),
        };
    }

    async openLoginPage(url) {
        await this.driver.get(url);
    }

    async login() {
        await this.driver.findElement(this.locators.user).sendKeys("student");
        await this.driver.findElement(this.locators.password).sendKeys("Password123");
        await this.driver.findElement(this.locators.loginButton).click();
    }
    }

    export default LoginPage;

            """)

            with open(os.path.join(pages_dir, "readme.md"), "w") as f:
                f.write(
                    "# JavaScript Boilerplate Project\n\n"
                    "This boilerplate project includes a basic setup for a JavaScript application using Selenium for automated browser testing.\n\n"
                    "## Setup\n\n"
                    "Follow the steps below to get started with this boilerplate:\n\n"
                    "1. Install Node.js and npm. You can download them [here](https://nodejs.org/).\n\n"
                    "```sh\n"
                    "npm install\n"
                    "```\n\n"
                    "## Usage\n\n"
                    "This boilerplate uses Selenium for browser automation. Tests are written with Mocha and make use of the Selenium WebDriver API.\n\n"
                    "To run the tests, use the command:\n\n"
                    "```sh\n"
                    "npm test\n"
                    "```\n\n"
                    "## Test Reports\n\n"
                    "Test results can be output in the XUnit format, which can be used as input to many testing tools and services:\n\n"
                    "```sh\n"
                    "mocha --reporter xunit --reporter-options output=results.xml\n"
                    "```\n"
                )


    def create_readme(self):
        with open('README.md', 'w') as f:
            f.write('# Selenium Python Project\n\n')
            f.write(
                'This is a boilerplate project for Selenium automation testing in Python.\n\n')

            f.write('## Requirements\n')
            f.write('Install all the dependencies from the `requirements.txt`:\n')
            f.write('```bash\n')
            f.write('pip install -r requirements.txt\n')
            f.write('```\n\n')

            f.write('## Directory Structure\n')
            f.write('- `tests`: This directory contains all the test scripts.\n')
            f.write('- `pages`: This directory contains all the page object models.\n')
            f.write(
                '- `utils`: This directory contains utility functions that are used across the project.\n\n')

            f.write('## How to Run Tests\n')
            f.write(
                'To run tests, navigate to the project directory and run the following command:\n')
            f.write('```bash\n')
            f.write('pytest\n')
            f.write('```\n')