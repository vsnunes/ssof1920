# Discovering vulnerabilities in Python web applications
Software Security project

## Useful Links
[Project Description](https://fenix.tecnico.ulisboa.pt/disciplinas/SSof7/2019-2020/1-semestre/project)

## Problem
A large class of vulnerabilities in applications originates in programs that enable user input information to affect the values of certain parameters of security sensitive functions. In other words, these programs encode an illegal information flow, in the sense that low integrity -- tainted -- information (user input) may interfere with high integrity parameters of sensitive functions (so called sensitive sinks). This means that users are given the power to alter the behavior of sensitive functions, and in the worst case may be able to induce the program to perform security violations.

Often, such illegal information flows are desirable, as for instance it is useful to be able to use the inputted user name for building SQL queries, so we do not want to reject them entirely. It is thus necessary to differentiate illegal flows that can be exploited, where a vulnerability exists, from those that are inoffensive and can be deemed secure, or endorsed, where there is no vulnerability. One approach is to only accept programs that properly sanitize the user input, and by so restricting the power of the user to acceptable limits, in effect neutralizing the potential vulnerability.

The aim of this project is to study how web vulnerabilities can be detected statically by means of taint and input sanitization analysis. We choose as a target web server side programs encoded in the Python language. There exist a [range of Web frameworks](https://wiki.python.org/moin/WebFrameworks) for Python, of which Django is the most widely used. While examples in this project specification often refer to [Django views](https://docs.djangoproject.com/en/2.2/topics/http/views/), the problem is to be understood as generic to the Python language.

The following references are mandatory reading about the problem:

* [J. Conti and A. Russo, "Taint Mode for Python via a Library", OWASP 2010](http://www.cse.chalmers.se/~russo/publications_files/owasp2010.pdf)
* [V. Chibotaru et. al, "Scalable Taint Specification Inference with Big Code", PLDI 2019](https://files.sri.inf.ethz.ch/website/papers/scalable-taint-specification-inference-pldi2019.pdf) **Note**: This paper contains a large component of machine learning that is not within the scope of this course, and which you may skip through.
* [S. Micheelsen and B. Thalmann, "PyT - A Static Analysis Tool for Detecting Security Vulnerabilities in Python Web Applications", Master?s Thesis, Aalborg University 2016](https://projekter.aau.dk/projekter/files/239563289/final.pdf)