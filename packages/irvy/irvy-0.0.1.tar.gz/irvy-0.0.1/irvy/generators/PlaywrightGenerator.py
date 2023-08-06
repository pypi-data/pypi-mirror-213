import os


class PlaywrightGenerator:
    def __init__(self, language):
        self.language = language

    def generate(self):
        if self.language == "csharp":
            self.create_csharp_playwright()
        elif self.language == "python":
            self.create_python_playwright_project()
            self.create_readme()
        elif self.language == "javascript":
            self.create_javascript_playwright_project()

    def create_csharp_playwright(self):
        os.system("dotnet new console -n PlaywrightCsharp")
        os.makedirs("PlaywrightCsharp/Tests")
        os.makedirs("PlaywrightCsharp/Pages")
        os.makedirs("PlaywrightCsharp/Utils")
        os.system("dotnet add package Microsoft.Playwright")
        os.system("dotnet add PlaywrightCsharp package NUnit")
        os.system("dotnet add PlaywrightCsharp package NUnit3TestAdapter")
        os.system("dotnet add PlaywrightCsharp package Microsoft.NET.Test.Sdk")
        os.system("dotnet tool install --global dotnet-reportgenerator-globaltool")
        
        with open("PlaywrightCsharp/readme.md", "w") as file:
            file.write("""
                       # PlaywrightCsharp

This project contains an example of automating web UI tests using Microsoft Playwright in C#.

## Project Structure

The project is structured into the following main folders:

- `Pages`: This folder contains classes for different pages of the web application under test. Each class encapsulates the operations that can be performed on a specific page.

- `Tests`: This folder contains NUnit test cases for testing features of the web application.

- `Utils`: This folder contains utility classes used across the project.

## Getting Started
Go to the new created folder

Run following command
´´´
dotnet test
´´´
### Prerequisites

- .NET SDK 7.0 or later
- Microsoft Playwright

                    
                    """)

        with open("PlaywrightCsharp/Utils/Configuration.cs", "w") as file:
            file.write("""
    namespace PlaywrightCsharp.Utils
    {
        public static class Configuration
        {
            public const string Url = "https://practicetestautomation.com/practice-test-login/";
            public const string Username = "student";
            public const string Password = "Password123";
            public const bool Headless = false;
        }

    }
    """)

        with open("PlaywrightCsharp/Pages/LoginPage.cs", "w") as file:
            file.write("""using System.Threading.Tasks;
    using Microsoft.Playwright;

    namespace PlaywrightCsharp.Pages
    {
        public class LoginPage
        {
            private readonly IPage page;

            public LoginPage(IPage page)
            {
                this.page = page;
            }

            public async Task EnterUsername(string username)
            {
                await page.TypeAsync("#username", username); 
            }

            public async Task EnterPassword(string password)
            {
                await page.TypeAsync("#password", password); // Update with the correct selector
            }

            public async Task ClickLoginButton()
            {
                await page.Locator("//*[@id='submit']").ClickAsync();
            }
        }
    }
    """)

        with open("PlaywrightCsharp/Tests/LoginTest.cs", "w") as file:
            file.write("""
    using System;
    using Microsoft.Playwright;
    using PlaywrightCsharp.Pages;
    using PlaywrightCsharp.Utils;
    using NUnit.Framework;
    using System.Threading.Tasks;

    namespace PlaywrightCsharp.Tests
    {
        [TestFixture]
        public class LoginTest
        {
            private IBrowser? browser;
            private IPage? page;
            private LoginPage? loginPage;

            [SetUp]
            public async Task SetUpAsync()
            {
                var playwright = await Playwright.CreateAsync();
                browser = await playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions { Headless = Configuration.Headless });
                page = await browser.NewPageAsync();
                loginPage = new LoginPage(page);

                await page.GotoAsync(Configuration.Url);
            }

            [Test]
            public async Task TestLogin()
            {
                await loginPage.EnterUsername(Configuration.Username);
                await loginPage.EnterPassword(Configuration.Password);
                await loginPage.ClickLoginButton();
                // TODO: Verify successful login
            }

            [TearDown]
            public async Task TeardownAsync()
            {
                await browser.CloseAsync();
            }
        }
    }
    """)

        with open("PlaywrightCsharp/Program.cs", "w") as file:
            file.write("""
    using System;

    namespace PlaywrightCsharp
    {
        class Program
        {
            static void IrvyTest(string[] args)
            {
                Console.WriteLine("Hello, irvy!");
            }
        }
    }

    """)

        # Change directory and add required packages
        os.chdir('PlaywrightCsharp')
        os.system("dotnet add package Microsoft.Playwright")
        os.system("dotnet build")
        os.chdir('..')  # go back to the original directory

   
   
    def create_python_playwright_project(self):
        os.mkdir('tests')
        os.mkdir('pages')
        os.mkdir('utils')

        with open('requirements.txt', 'w') as f:
            f.write('pytest-playwright\n')

        os.system("playwright install")

        with open('pages/__init__.py', 'w') as f:
            f.write('')

        with open('utils/__init__.py', 'w') as f:
            f.write('')

        with open('tests/__init__.py', 'w') as f:
            f.write('')

        with open("tests/test_login.py", "w") as f:
            f.write("""from pages.login_page import LoginPage
    def test_login():
        login_page = LoginPage()
        login_page.navigate()
        login_page.login('user', 'password')
    """)

            # Generate login_page.py
            with open("pages/login_page.py", "w") as f:
                f.write("""from playwright.sync_api import sync_playwright

    class LoginPage:
        def __init__(self):
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch()
            self.page = self.browser.new_page()

        def navigate(self):
            self.page.goto('https://practicetestautomation.com/practice-test-login/')

        def login(self, username, password):
            self.page.fill('#username', username)
            self.page.fill('#password', password)
            self.page.click('#login')

        def __del__(self):
            self.browser.close()
            self.playwright.stop()
    """)


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

    def create_javascript_playwright_project(self):
        # Create necessary directories
        os.system("mkdir PlaywrightJavaScript")
        os.chdir("PlaywrightJavaScript")
        os.system("mkdir tests pages utils")

        # Create package.json for Node.js project
        with open('package.json', 'w') as f:
            f.write("""{
            "name": "playwright-javascript",
            "version": "1.0.0",
            "description": "",
            "main": "index.js",
            "scripts": {
                "test": "mocha tests/*.js --timeout 10000"
            },
            "dependencies": {
                "chai": "^4.3.7",
                "mocha": "^10.2.0",
                "playwright": "^1.16.3"
            }
        }
        
        """)

        # Create a config file
        with open('config.js', 'w') as f:
            f.write("""
        module.exports = {
            url:"https://practicetestautomation.com/practice-test-login/",
            username: "student",
            password: "Password123",
            headless: false // whether to run browser in headless mode
        };
        """)

        # Create a test script in the tests directory
        with open('tests/login_test.js', 'w') as f:
            f.write("""
    const { expect } = require('chai');
    const LoginPage = require('../pages/LoginPage');
    const config = require('../config');

    describe('Login Test', () => {
    let loginPage;

    before(async () => {
        loginPage = new LoginPage(config.headless);
        console.log(config.url);
        await loginPage.navigate(config.url);
    });

    it('should log in successfully', async () => {
        await loginPage.login(config.username, config.password) 
        //await loginPage.submit();
    });

    after(async () => {
        await loginPage.close();
    });
    });

    """)

        # Create a login page file
            with open('pages/LoginPage.js', 'w') as f:
                f.write("""
    const { chromium } = require('playwright');

    const isHeadless = false

    class LoginPage {
        constructor(headless) {
            this.isHeadless = headless;
            this.browser = null;
            this.page = null;
        }

        async navigate(url) {
            this.browser = await chromium.launch({ headless: isHeadless });
            const context = await this.browser.newContext();
            this.page = await context.newPage();
            await this.page.goto(url);  // replace with your actual login page URL
        }

        async login(username, password) {
            await this.page.type('#username', username);  // replace with actual username field selector
            await this.page.type('#password', password);  // replace with actual password field selector
            await this.page.click('#submit');  // replace with actual submit button selector
        }
        
        async close() {
            await this.browser.close();
        }
    }

    module.exports = LoginPage;

        """)

    # Create README.md
    with open('README.md', 'w') as f:
        f.write('# Playwright JavaScript Project\n\n')
        f.write(
            'This is a boilerplate project for Playwright automation testing in JavaScript.\n\n')
        f.write('## Requirements\n')
        f.write('Install all the dependencies from the `package.json`:\n')
        f.write('```bash\n')
        f.write('npm install\n')
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
        f.write('npm test\n')
        f.write('```\n')