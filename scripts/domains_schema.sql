

CREATE TABLE `rankdb` (
  `rank` int(11) NOT NULL,
  `domain` text NOT NULL,
  `pagerank` float NOT NULL,
  `title` text DEFAULT NULL,
  PRIMARY KEY (`domain`(200))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


