<a name="readme-top"></a>

<!-- VideoPoker-5CardRedraw -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ralbee1/VideoPoker-5CardRedraw">
    <img src="documentation/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">VideoPoker-5CardRedraw</h3>

  <p align="center">
    A pythonic creation of a 5 card redraw video poker.
    <br />
    <a href="https://github.com/ralbee1/VideoPoker-5CardRedraw"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ralbee1/VideoPoker-5CardRedraw">View Demo</a>
    ·
    <a href="https://github.com/ralbee1/VideoPoker-5CardRedraw/issues">Report Bug</a>
    ·
    <a href="https://github.com/ralbee1/VideoPoker-5CardRedraw/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#Features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
<!-- 
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->
5 Card Draw is a playable Python 5-card draw poker application. This project served as a hands-on Python learning experience in 2021. On my journey, I learned about creating graphical user interfaces in Python, pythonic best practices, CI/CD workflows, PyPi deployments, and much more. The beautiful learning opportunity this project provided was balancing desired learning opportunities and refining 5 Card Draw into a polished application. This project archived with the last remaining features involved in further polishing the UI/UX experience, adding sound, and cashing out player credits. If I were to start over, I'd rank poker hands with a semantic system over an integer score.
 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Features

- [ ] **5 Card Redraw**
  - [ ] Modular Hand Ranking and Scoring
  - [ ] Player Hand and Deck creation
  - [ ] Playable GUI interface
  - [ ] Bank text file
- [ ] **PyPi Installs**
- [ ] **Pep 8 Standards**
- [ ] **GitHub CI/CD Pipelines**

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

The following is an guide for running 5 card redraw poker locally.

### Prerequisites

1. [Python 3.10.8 or Newer](https://www.python.org/downloads/release/python-3108/)


### Installation

Local Repo Install:
<br/>
Summary: The developer install is for those who want to contribute to or clone VideoPoker-5CardRedraw.
1. Clone the repo (or use Github Desktop)
   ```sh
   git clone https://github.com/ralbee1/5_card_draw.git
   ```
2. Open the CLI and navigate the current working directory to where you cloned VideoPoker-5CardDraw
3. Install the Pip Package from the CLI, copy and run this command:
   ```sh
   py -m pip install -e .
   ```
<br/>
<br/>
User Install
<br/>
1. Automatic User Install from the Command line via PyPi.
   ```sh
   pip install five-card-draw
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage / How to Play
If your python files open with Python by default then from the commmand line run:

  ```js
  poker_start.py;
  ```

Troubleshooting:
1. "'poker_start.py' is not recognized as an internal or external command, operable program or batch file."
  Your terminal needs to be able to find the file. For windows, you need to ensure your python "script" folder is in your path variable
  For example: C:\Users\{username}\AppData\Roaming\Python\{pythonversion}\Scripts
  You may also navigate to where the pip was installed and run poker_start.py with python manually.

The game is played by aiming to make the best poker hand possible. The top of the interface shows the hand ranking and the payouts sorted by how many credits you bet per round, 1 thru 5. To begin, click DEAL. You hold cards with the intent of keeping them and drawing new cards to try to improve your hand ranking. After drawing new cards, your hand is automatically scored and profits paid out. You may then click "DEAL" and start over.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

* []()Email - ralbee1@iwu.edu
* []()Project Link: [https://github.com/ralbee1/VideoPoker-5CardRedraw](https://github.com/ralbee1/VideoPoker-5CardRedraw)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []() This variant of poker was inspired by Super Double Double as found in Las Vegas Casinos.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ralbee1/VideoPoker-5CardRedraw.svg?style=for-the-badge
[contributors-url]: https://github.com/ralbee1/VideoPoker-5CardRedraw/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ralbee1/VideoPoker-5CardRedraw.svg?style=for-the-badge
[forks-url]: https://github.com/ralbee1/VideoPoker-5CardRedraw/network/members
[stars-shield]: https://img.shields.io/github/stars/ralbee1/VideoPoker-5CardRedraw.svg?style=for-the-badge
[stars-url]: https://github.com/ralbee1/VideoPoker-5CardRedraw/stargazers
[issues-shield]: https://img.shields.io/github/issues/ralbee1/VideoPoker-5CardRedraw.svg?style=for-the-badge
[issues-url]: https://github.com/ralbee1/VideoPoker-5CardRedraw/issues
[license-shield]: https://img.shields.io/github/license/ralbee1/VideoPoker-5CardRedraw.svg?style=for-the-badge
[license-url]: https://github.com/ralbee1/VideoPoker-5CardRedraw/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/Richard-Albee
[product-screenshot]: images/screenshot.png
[python.org]: https://www.python.org/static/img/python-logo.png
[python-url]: https://www.python.org/
[pypi.org]: https://pypi.org/static/images/logo-small.2a411bc6.svg
[pypi-url]: https://pypi.org/project/pip/
