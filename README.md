# LinkedIn Profile Scraper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A Python package for scraping LinkedIn profile data. This package allows you to easily extract structured data from LinkedIn profiles using Playwright for browser automation.

## 🚀 Features

- **Complete Profile Data**: Extract comprehensive profile information including:
  - Basic profile details (name, headline, location, etc.)
  - Work experience with company details
  - Education history
  - Skills and endorsements
  - Projects
  - Languages
  - Licenses and certifications
  - And more
- **Human-like Browsing**: Advanced browser automation techniques to avoid detection
- **Flexible Authentication**: Configure via environment variables or direct parameters
- **Async Architecture**: Built with asyncio for efficient scraping
- **Simple API**: Easy-to-use functions with comprehensive documentation
- **Command-line Interface**: Use directly from the terminal

## 📋 Prerequisites

- Python 3.7+
- A LinkedIn account
- Playwright (installed automatically with the package)

## 🔧 Installation

### From GitHub

```bash
pip install git+https://github.com/neerajmenon/linkedin-scraper.git
```

### Development Installation

```bash
git clone https://github.com/neerajmenon/linkedin-scraper.git
cd linkedin-scraper
pip install -e .
```

### Installing Playwright Browsers

After installation, you need to install the Playwright browsers:

```bash
playwright install chromium
```

## 📖 Usage

### Basic Usage

```python
import asyncio
import os
from linkedin_scraper import scrape_linkedin_profile

# Set LinkedIn credentials as environment variables
os.environ['LINKEDIN_EMAIL'] = 'your_linkedin_email@example.com'
os.environ['LINKEDIN_PASSWORD'] = 'your_linkedin_password'

# Profile URL to scrape
profile_url = 'https://www.linkedin.com/in/username/'

# Scrape the profile
async def main():
    profile_data = await scrape_linkedin_profile(profile_url)
    print(profile_data)

# Run the async function
asyncio.run(main())
```

### Passing Credentials Directly

```python
import asyncio
from linkedin_scraper import scrape_linkedin_profile

async def main():
    profile_data = await scrape_linkedin_profile(
        'https://www.linkedin.com/in/username/',
        email='your_linkedin_email@example.com',
        password='your_linkedin_password'
    )
    print(profile_data)

asyncio.run(main())
```

### Saving Profile Data to JSON

```python
import asyncio
from linkedin_scraper import save_profile_to_json

async def main():
    success = await save_profile_to_json(
        'https://www.linkedin.com/in/username/',
        output_file='profile_data.json',
        email='your_linkedin_email@example.com',
        password='your_linkedin_password'
    )
    
    if success:
        print("Profile data saved successfully!")

asyncio.run(main())
```

### Command Line Usage

You can also use the package directly from the command line:

```bash
# Using environment variables for credentials
export LINKEDIN_EMAIL='your_linkedin_email@example.com'
export LINKEDIN_PASSWORD='your_linkedin_password'
python -m linkedin_scraper https://www.linkedin.com/in/username/ --output profile_data.json

# Or passing credentials directly (not recommended for security reasons)
python -m linkedin_scraper https://www.linkedin.com/in/username/ --email your_email@example.com --password your_password --output profile_data.json
```

## 🔍 Example Output

The scraper returns a structured JSON object with profile data:

```json
{
  "name": "John Doe",
  "headline": "Senior Software Engineer at Example Corp",
  "location": "San Francisco Bay Area",
  "summary": "Experienced software engineer with a passion for...",
  "experience": [
    {
      "title": "Senior Software Engineer",
      "company": "Example Corp",
      "date_range": "Jan 2020 - Present",
      "location": "San Francisco, CA",
      "description": "Leading development of..."
    }
  ],
  "education": [
    {
      "school": "University of California, Berkeley",
      "degree": "Bachelor of Science, Computer Science",
      "date_range": "2012 - 2016"
    }
  ],
  "skills": ["Python", "JavaScript", "React", "Node.js"],
  "languages": ["English (Native)", "Spanish (Professional)"],
  "certifications": ["AWS Certified Solutions Architect"]
}
```

## 🛡️ Security Considerations

- **Never hardcode** your LinkedIn credentials in your code
- Use **environment variables** or a secure configuration management system
- Consider using a **dedicated LinkedIn account** for scraping to avoid potential account restrictions
- Be aware that excessive scraping may lead to **temporary IP blocks**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Scraping LinkedIn may violate their Terms of Service. Use at your own risk and responsibility. The authors are not responsible for any misuse of this software or any violations of LinkedIn's terms of service.
