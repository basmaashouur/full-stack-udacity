import media
import fresh_tomatoes


def get_movies():
    """ function make an instance from Movie class to represent a movie """
    imitation_game = media.Movie(
                           "The Imitation Game",
                           "Story about Alan Turing to crack Nazi codes.",
                           "https://goo.gl/C3Jatc",
                           "https://www.youtube.com/watch?v=S5CjKEFb-sM&t=32s")

    storyof_evrything = media.Movie(
                            "The Theory of Everything",
                            "Story about the physicist Stephen Hawking.",
                            "https://goo.gl/PDuwsm",
                            "https://www.youtube.com/watch?v=Salz7uGp72c&t=3s")
    knew_inf = media.Movie(
                    "The Man Who Knew Infinity",
                    "Story about Ramanujan travels to Trinity College.",
                    "https://goo.gl/79Qmot",
                    "https://www.youtube.com/watch?v=oXGm9Vlfx4w&t=16s")
    hidden_figures = media.Movie(
                           "Hidden Figures",
                           "Story about brilliant African-American women.",
                           "https://goo.gl/s18NQC",
                           "https://www.youtube.com/watch?v=5wfrDhgUMGI")          
    beautiful_mind = media.Movie(
                           "A Beautiful Mind",
                           "Story about the mathematical John Forbes Nas.",
                           "https://goo.gl/HPQuUm",
                           "https://www.youtube.com/watch?v=aS_d0Ayjw4o")
    concussion = media.Movie(
                       "Concussion",
                       "Story about Dr. Bennet Omalu.",
                       "https://goo.gl/fYDy2W",
                       "https://www.youtube.com/watch?v=LVRIntuk7uc")
    movies = [imitation_game, storyof_evrything,
              knew_inf, beautiful_mind, hidden_figures, concussion]
    return movies


def main():
    """ main function """
    movies = get_movies()
    fresh_tomatoes.open_movies_page(movies)

main()
