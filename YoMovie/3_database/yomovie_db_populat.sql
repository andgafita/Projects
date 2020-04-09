-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Gazdă: 127.0.0.1
-- Timp de generare: iun. 13, 2019 la 09:09 AM
-- Versiune server: 10.3.15-MariaDB
-- Versiune PHP: 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Bază de date: `yomovie_db`
--

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `actors`
--

CREATE TABLE `actors` (
  `id` int(11) NOT NULL,
  `nume` varchar(15) NOT NULL,
  `prenume` varchar(25) NOT NULL,
  `varsta` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Eliminarea datelor din tabel `actors`
--

INSERT INTO `actors` (`id`, `nume`, `prenume`, `varsta`) VALUES
(1, 'Reeves', 'Keanu', 33),
(2, 'Pitt', 'Brad', 40),
(3, 'Cruise', 'Tom', 56);

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `badges`
--

CREATE TABLE `badges` (
  `id` int(11) NOT NULL,
  `icon_path` varchar(100) DEFAULT NULL,
  `title` varchar(30) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `movie_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Eliminarea datelor din tabel `badges`
--

INSERT INTO `badges` (`id`, `icon_path`, `title`, `description`, `movie_id`) VALUES
(0, NULL, NULL, NULL, 0),
(1, 'illustration-lock-icon_53876-5633.jpg', 'Inchizator', 'Felicitari! Ai ales sa inchizi geamul.', 2),
(2, 'unlock-icon.PNG', 'Deschizator', 'Bravo! Ai ales sa deschizi geamul.', 3),
(3, 'asd.PNG', 'Alegatorul', 'Ai ales choice-ul 1.', 5);

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `choices`
--

CREATE TABLE `choices` (
  `id` int(11) NOT NULL,
  `descriere` varchar(100) DEFAULT NULL,
  `text_intrebare` varchar(100) DEFAULT NULL,
  `clip_path` varchar(128) DEFAULT NULL,
  `id_precedent` int(11) DEFAULT NULL,
  `movie_id` int(11) DEFAULT NULL,
  `choice_number` int(11) DEFAULT NULL,
  `badge_id` int(11) DEFAULT NULL,
  `vizualizari` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Eliminarea datelor din tabel `choices`
--

INSERT INTO `choices` (`id`, `descriere`, `text_intrebare`, `clip_path`, `id_precedent`, `movie_id`, `choice_number`, `badge_id`, `vizualizari`) VALUES
(0, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0),
(1, NULL, 'Ce vrei sa faci cu geamul?', 'initial.mp4', 0, 1, NULL, NULL, 1),
(2, 'Inchide-l', '', 'inchis.mp4', 1, 1, 1, 1, 1),
(3, 'Deschide-l', '', 'deschis.mp4', 1, 1, 2, 2, 0),
(4, NULL, 'Exemplu de intrebare cu 5 raspunsuri?', '20190605_170836.mp4', 0, 2, NULL, NULL, 0),
(5, '1', '', 'deschis.mp4', 4, 2, 1, 3, 0),
(6, '2', NULL, NULL, 4, 2, 2, NULL, 0),
(7, '3', NULL, NULL, 4, 2, 3, NULL, 0),
(8, '4', NULL, NULL, 4, 2, 4, NULL, 0),
(9, '5', NULL, NULL, 4, 2, 5, NULL, 0);

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `distribution`
--

CREATE TABLE `distribution` (
  `movie_id` int(11) NOT NULL,
  `actor_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Eliminarea datelor din tabel `distribution`
--

INSERT INTO `distribution` (`movie_id`, `actor_id`) VALUES
(1, 1),
(2, 1),
(1, 2),
(2, 3);

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `movies`
--

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `clip_id` int(11) NOT NULL,
  `uploader_id` int(11) DEFAULT NULL,
  `title` varchar(25) NOT NULL,
  `rating` float NOT NULL,
  `votes` int(11) NOT NULL,
  `upload_date` date NOT NULL,
  `thumbnail_path` varchar(128) NOT NULL,
  `genre` varchar(20) NOT NULL,
  `description` varchar(200) NOT NULL,
  `views` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Eliminarea datelor din tabel `movies`
--

INSERT INTO `movies` (`id`, `clip_id`, `uploader_id`, `title`, `rating`, `votes`, `upload_date`, `thumbnail_path`, `genre`, `description`, `views`) VALUES
(0, 0, 0, '', 0, 0, '0000-00-00', '', '', '', 0),
(1, 1, 1, 'Primul film', 5, 1, '2019-06-13', 'thumbnail1.jpg', 'Drama', 'Acesta este primul meu film.', 3),
(2, 4, 2, 'Un alt film', 0, 0, '2019-06-13', 'thumbnail2.jpg', 'Comedy', 'Acesta este al doilea film.', 0);

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `rewards`
--

CREATE TABLE `rewards` (
  `user_id` int(11) NOT NULL,
  `badge_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Eliminarea datelor din tabel `rewards`
--

INSERT INTO `rewards` (`user_id`, `badge_id`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(30) NOT NULL,
  `parola` varchar(40) NOT NULL,
  `username` varchar(20) NOT NULL,
  `session_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Eliminarea datelor din tabel `users`
--

INSERT INTO `users` (`id`, `email`, `parola`, `username`, `session_id`) VALUES
(0, '', '', '', NULL),
(1, 'asocriss@gmail.com', 'f10e2821bbbea527ea02200352313bc059445190', 'asocris', NULL),
(2, 'andrei@yahoo.com', '3da541559918a808c2402bba5012f6c60b27661c', 'andrei', NULL);

--
-- Indexuri pentru tabele eliminate
--

--
-- Indexuri pentru tabele `actors`
--
ALTER TABLE `actors`
  ADD PRIMARY KEY (`id`);

--
-- Indexuri pentru tabele `badges`
--
ALTER TABLE `badges`
  ADD PRIMARY KEY (`id`),
  ADD KEY `badges_ibfk_1` (`movie_id`);

--
-- Indexuri pentru tabele `choices`
--
ALTER TABLE `choices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `movie_id` (`movie_id`),
  ADD KEY `id_precedent` (`id_precedent`);

--
-- Indexuri pentru tabele `distribution`
--
ALTER TABLE `distribution`
  ADD PRIMARY KEY (`actor_id`,`movie_id`),
  ADD KEY `distribution_ibfk_2` (`movie_id`);

--
-- Indexuri pentru tabele `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `uploader_id` (`uploader_id`);

--
-- Indexuri pentru tabele `rewards`
--
ALTER TABLE `rewards`
  ADD PRIMARY KEY (`user_id`,`badge_id`),
  ADD KEY `badge_id` (`badge_id`);

--
-- Indexuri pentru tabele `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Constrângeri pentru tabele eliminate
--

--
-- Constrângeri pentru tabele `badges`
--
ALTER TABLE `badges`
  ADD CONSTRAINT `badges_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `choices` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constrângeri pentru tabele `choices`
--
ALTER TABLE `choices`
  ADD CONSTRAINT `choices_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `choices_ibfk_2` FOREIGN KEY (`id_precedent`) REFERENCES `choices` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constrângeri pentru tabele `distribution`
--
ALTER TABLE `distribution`
  ADD CONSTRAINT `distribution_ibfk_1` FOREIGN KEY (`actor_id`) REFERENCES `actors` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `distribution_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constrângeri pentru tabele `movies`
--
ALTER TABLE `movies`
  ADD CONSTRAINT `movies_ibfk_1` FOREIGN KEY (`uploader_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Constrângeri pentru tabele `rewards`
--
ALTER TABLE `rewards`
  ADD CONSTRAINT `rewards_ibfk_1` FOREIGN KEY (`badge_id`) REFERENCES `badges` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `rewards_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
