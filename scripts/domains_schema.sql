CREATE TABLE `rankdb` (
  `rank` int(11) NOT NULL,
  `domain` text NOT NULL,
  `pagerank` float NOT NULL,
  `title` text DEFAULT NULL,
  PRIMARY KEY (`domain`(200))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `domainrisk`.`domainpage` (
  `domain` TEXT NOT NULL,
  `tohost` TEXT NOT NULL,
  `todomain` TEXT NOT NULL,
  `updated` DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expiry` date NOT NULL,
  `issuer_org` varchar(100) NOT NULL,
  INDEX `tohost` (`tohost`),
  INDEX (`todomain`)
) ENGINE = InnoDB;
