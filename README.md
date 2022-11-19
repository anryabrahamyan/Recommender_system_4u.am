# Recommendation System for 4u.am

The recommendation system for 4u.am helps people who use 4u.am and want to get personalized recommendations and make correct decisions in their online shopping. Our main users are people who already use 4u.am, or are starting to use online shopping tools. For 4u.am the recommendation system will increase sales and redefine the users' web browsing experience, retain the customers, and enhance their shopping experience.

## Installation

Make sure to have the packages in the requirement.txt, e.g.

```python
pip install pandas
```
## Running the app

In order to run the code:
```python
python app.py
```

## Low-Fidelity Mockup

You can find the skeleton of the future app [here](https://www.figma.com/file/sCU4n4i3felNCzD73lxvFe/Low-fidelity-mockup?node-id=1%3A6).

## Roadmap

You can find the roadmap of our project [here]( https://www.figma.com/file/CreZVKPt76Gb8v86KLdRwE/Group-5-Roadmap?node-id=0%3A1).

## Recommendation system Testing

First of all you need to fetch and download content from our remote repository with

```python 
git pull
```

Then change your directory to Recommender_system_4u.am/

```python 
cd  Recommender_system_4u.am/
```


Then you need to get the scraped data with 
```python 
python src/scraper.py
```

Then in order to 
- clean the data,
- download the images into a new directory (images), 
- put the vectorized product names, descriptions and images into the corresponding .npy files in the data directory 

```python 
python src/create_recommendation_dataset.py
```

Finally to get the recommended 5 products for each product

```python 
python src/recommender.py
```

(In the recommender.py’s main function the product for which you’ll get the recommendations is the first product in our 
data, in order to change it, just put your desired number(0-296) instead of 0 in

```python 
print(rec.predict(0)) 
```
