
CREATE TABLE `rankdb` (
  `rank` int(11) NOT NULL,
  `domain` text NOT NULL,
  `pagerank` float NOT NULL,
  `title` text DEFAULT NULL,
  `last_updated` date NOT NULL DEFAULT current_timestamp(),
  `cert_expiry` date DEFAULT NULL,
  `cert_issuer` varchar(100) DEFAULT NULL,
  `last_checked` date DEFAULT NULL,
  PRIMARY KEY (`domain`(200)),
  KEY `cert_issuer` (`cert_issuer`),
  KEY `rank` (`rank`),
  KEY `rank_2` (`rank`),
  KEY `last_checked_index` (`last_checked`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci


CREATE TABLE `domainpage` (
  `domain` text NOT NULL,
  `tohost` text NOT NULL,
  `todomain` text NOT NULL,
  `updated` date NOT NULL DEFAULT current_timestamp(),
  KEY `tohost` (`tohost`(768)),
  KEY `todomain` (`todomain`(768))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
