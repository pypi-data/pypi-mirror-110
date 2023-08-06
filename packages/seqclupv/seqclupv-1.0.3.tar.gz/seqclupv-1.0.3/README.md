<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** rtewierik, seqclupv, twitter_handle, email, project_title, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/rtewierik/seqclupv"></a>

  <h3 align="center">SeqCluPV - Real-time sequence clustering using prototype voting</h3>
  <p align="center">
    <a href="https://github.com/rtewierik/seqclupv"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/rtewierik/seqclupv/issues">Report bug</a>
    ·
    <a href="https://github.com/rtewierik/seqclupv/issues">Request feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About the project</a>
      <ul>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About the project
This project, called *SeqCluPV* is an extension of the original *SeqClu* algorithm, developed by Dr.ir. Sicco Verwer of the *Delft University of Technology*, that is characterized by voting for cluster prototypes. The framework has been developed as part of the course *CSE3000 Research Project* at the *Delft University of Technology*. For instructions on how to get a local copy up and running, please refer to the [Getting started](#getting-started) section.


### Built with

* [NumPy](https://pypi.org/project/numpy/)
* [FastDTW](https://pypi.org/project/fastdtw/)
* [SciPy](https://pypi.org/project/scipy/)
* [Pandas](https://pypi.org/project/pandas/)
* [Scikit-learn](https://pypi.org/project/scikit-learn/)
* [Seaborn](https://pypi.org/project/seaborn/)
* [Matplotlib](https://pypi.org/project/matplotlib/)



<!-- GETTING STARTED -->
## Getting started

To get a local copy up and running follow these simple steps.

### Prerequisites

The project was made with Python 3.9, hence having Python 3.9 installed is a prerequisite.

### Installation from PyPI

1. Install Cython
   ```
   pip install Cython
   ```
2. Clone the *sktime* repository in a separate directory
   ```
   git clone https://github.com/alan-turing-institute/sktime.git
   ```
3. After navigating to the *sktime* project root, install *sktime*
   ```
   python setup.py install
   ```
4. Install *SeqCluPV*
   ```
   pip install seqclupv
   ```

### Installation from source

1. Clone the repo
   ```
   git clone https://github.com/rtewierik/seqclupv.git
   ```
2. Install Cython
   ```
   pip install Cython
   ```
3. Clone the *sktime* repository in a separate directory
   ```
   git clone https://github.com/alan-turing-institute/sktime.git
   ```
4. After navigating to the *sktime* project root, install *sktime*
   ```
   python setup.py install
   ```
5. After navigating to the *SeqCluPV* project root, install *SeqCluPV*
   ```
   python setup.py install
   ```



<!-- USAGE EXAMPLES -->
## Usage

The algorithm can be run on three data sets, which are the following.

1. GesturePebbleZ1 (http://www.timeseriesclassification.com/description.php?Dataset=GesturePebbleZ1)
2. UJI Pen Characters (https://archive.ics.uci.edu/ml/datasets/UJI+Pen+Characters)
3. PLAID (http://www.timeseriesclassification.com/description.php?Dataset=PLAID)

The command-line interface can be used as follows.

<pre>
python -m seqclupv <i>numPrototypes</i> <i>numRepresentativePrototypes</i> <i>maxPerTick</i> <i>dataSourceParameters</i> <i>seqCluParameters</i> <i>maxIter</i> <i>online</i> <i>onlySeqClu</i> <i>experimentName</i>
</pre>

The potential values for the above parameters are as follows.

* **numPrototypes:** *integer* - The number of prototypes that will be used by all variants of the algorithm.
* **numRepresentativePrototypes:** *integer* - The number of representative prototypes that will be used by all variants of the algorithm.
* **maxPerTick:** *integer* - The maximum amount of sequences that can be processed per tick.
* **dataSourceParameters:** *list\[character\]* or *list\[boolean,string\]* - The two data sources that can be used are the handwritten character data source and the data source for the data sets from *TimeSeriesClassification.com*. For the handwritten character data source, this parameter is a JSON-formatted list of characters, where you can choose from the characters *\['C', 'U', 'V', 'W', 'S', 'O', '1', '2', '3', '5', '6', '8', '9'\]*. For the data sets from *TimeSeriesClassification.com*, this parameter is a list with two items, namely a boolean and a string in that order. The boolean value indicates whether or not the pair-wise distances between all items in the data set should be computed upfront, the string represents the name of the data set that is used. This string can be either of *\[\\"pebble\\",\\"plaid\\"\]*. **NOTE: Since the list is JSON-formatted, the boolean values should be either *true* or *false*. Moreover, spaces are NOT allowed.**
* **seqCluParameters:** *list\[integer, float, float, boolean, boolean\]* - The values in the list represent the following parameters in that order.
  * **bufferSize:** *integer* - The maximum size of the buffer.
  * **minimumRepresentativeness:** - *float* - The minimum average representativeness that prototypes should have in order for the distance computation from a sequence to the cluster that the prototypes represent to be approximated.
  * **prototypeValueratio:** - *float* - The value 'a' in a:1 where a:1 is the ratio between the representativeness and the weight. This ratio is used to compute the value of a prototype as a linear combination of the representativeness and the weight of the prototype.
  * **clusterAssignment:** - *boolean* - A boolean value indicating whether or not to approximate the distance to the cluster. **NOTE: Since the list is JSON-formatted, the boolean values should be either *true* or *false*. Moreover, spaces are NOT allowed.**
  * **buffering:** - *boolean* - A boolean value indicating whether or not the buffering feature should be used. **NOTE: Since the list is JSON-formatted, the boolean values should be either *true* or *false*. Moreover, spaces are NOT allowed.**
* **maxIter:** *integer* - The maximum number of iterations that the offline baseline variant of the algorithm is allowed to execute. **NOTE: This parameter is only needed when *online* and *onlySeqClu* are set to *False*, in other cases any integer is fine and the input will be ignored.**
* **online:** *boolean* - A boolean value that will result in executing the online baseline variant of the SeqClu algorithm if set to true and the offline baseline variant of the algorithm if set to false. **NOTE: Only the values 'True' or 'False' are possible here.**
* **onlySeqClu:** *boolean* - A boolean value indicating whether or not only the SeqClu algorithm should be executed. **NOTE: Only the values 'True' or 'False' are possible here.**
* **experimentName:** *string* - The name of the experiment. This is used to compare the prototypes at the end of executing (online baseline variant of) the SeqClu algorithm. The possible values can be *o29*, *o295w* and *pebbleFull*.

A few examples of commands that are executed to run specific experiments are as follows.

**Experiment with characters O, 2 and 9 of handwritten character data set using both the SeqClu algorithm and the online baseline variant of the SeqClu algorithm**
```
python -m seqclupv 8 3 1 [\"O\",\"2\",\"9\"]  [15,0.5,2.0,false,true] 0 True True o29
```


**Experiment with Pebble data set using just the SeqClu algorithm**
```
python -m seqclupv 8 3 1 [false,\"pebble\"]  [15,0.5,3.0,true,false] 0 True True pebbleFull
```


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/rtewierik/seqclupv/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

R.E.C. te Wierik - rtewierik64@gmail.com

Project link: [https://github.com/rtewierik/seqclupv](https://github.com/rtewierik/seqclupv)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [README template](https://github.com/othneildrew/Best-README-Template)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/rtewierik/seqclupv.svg?style=for-the-badge
[contributors-url]: https://github.com/rtewierik/seqclupv/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/rtewierik/seqclupv.svg?style=for-the-badge
[forks-url]: https://github.com/rtewierik/seqclupv/network/members
[stars-shield]: https://img.shields.io/github/stars/rtewierik/seqclupv.svg?style=for-the-badge
[stars-url]: https://github.com/rtewierik/seqclupv/stargazers
[issues-shield]: https://img.shields.io/github/issues/rtewierik/seqclupv.svg?style=for-the-badge
[issues-url]: https://github.com/rtewierik/seqclupv/issues
[license-shield]: https://img.shields.io/github/license/rtewierik/seqclupv.svg?style=for-the-badge
[license-url]: https://github.com/rtewierik/seqclupv/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/rtewierik/
