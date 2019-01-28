# ScenicTextSearch

The ScenicTextSearch searches for text in a picture and searches for the text on google.
It requires active internet connection.


# Getting Started

1.Clone the repository.

2.Add the tesseract package using the following command line-

```
pip install pytesseract
```

3.Add the imutils package using-

```
pip install imutils
```

4.Add the google search package using the following command line-

```
pip install beautifulsoup4
pip install google
```

5.Download the file from the given link in Download.md file to the cloned repository location.


# Using the code

1.Add the iamge file path to the line number 15 in the code.

2.**(Optional)** Change the padding level on the line number 125 and 126 accordingly.

3.**(Optional)** Change the new width and height of the input image on line number 32.

4.**(Optional)** Change the threshold value to discard the detected text boxes on line number 67.


# An Example

![1](https://user-images.githubusercontent.com/31141798/51114496-7d846600-182b-11e9-8f98-47f15b46d6d0.jpg)


## Detected Text

![capture](https://user-images.githubusercontent.com/31141798/51114654-f4216380-182b-11e9-8283-b2acb0fbff00.PNG)

## Search Results on console

![1](https://user-images.githubusercontent.com/31141798/51114813-6c882480-182c-11e9-8083-c10f3fd965a9.png)

## Search results on google webpage

![2](https://user-images.githubusercontent.com/31141798/51114819-73169c00-182c-11e9-8124-fac29d1059cd.png)


# Built With-

1. East Text Detector- to detect the bounding boxes or possible text regions

2. Tesseract- to convert the text boxes to strings

3. Google Search- to search for the string on the web crawler

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details


