import media
import fresh_tomatoes

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
                     "Story about Ramanujan travels to Trinity College in England..",
                     "https://goo.gl/79Qmot",
                     "https://www.youtube.com/watch?v=oXGm9Vlfx4w&t=16s")

beautiful_mind = media.Movie(
                           "A Beautiful Mind",
                           "Story about the mathematical genius f John Forbes Nash Jr.",
                           "https://goo.gl/HPQuUm",
                           "https://www.youtube.com/watch?v=aS_d0Ayjw4o")

hidden_figures = media.Movie(
                           "Hidden Figures",
                           "Story about three brilliant African-American women at NASA.",
                           "https://goo.gl/s18NQC",
                           "https://www.youtube.com/watch?v=5wfrDhgUMGI")

concussion = media.Movie(
                       "Concussion",
                       "Story about Dr. Bennet Omalu.",
                       "https://goo.gl/fYDy2W",
                       "https://www.youtube.com/watch?v=LVRIntuk7uc")

movies = [imitation_game, storyof_evrything, knew_inf, beautiful_mind, hidden_figures, concussion]
fresh_tomatoes.open_movies_page(movies)
