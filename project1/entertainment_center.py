import media
import fresh_tomatoes
import csv


def get_movies():
    """ make an instance from Movie class and put """
    """ the movie data from cvc file to represent a movie"""
    movies = []
    with open('names.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            movies.append(media.Movie(line[0], line[1], line[2], line[3]))
    return movies


def main():
    """ main function """
    movies = get_movies()
    fresh_tomatoes.open_movies_page(movies)

main()
