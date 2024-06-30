CREATE TABLE `domainpage` (
  `rankdb_id` bigint(20) NOT NULL,
  `tohost` char(200) NOT NULL,
  `todomain` char(200) NOT NULL,
  `last_updated` datetime NOT NULL DEFAULT current_timestamp(),
  KEY `todomain` (`todomain`) USING BTREE,
  KEY `tohost` (`tohost`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `rankdb` (
  `rank` int(11) NOT NULL,
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `domain` char(200) NOT NULL,
  `pagerank` float NOT NULL,
  `created_date` datetime NOT NULL DEFAULT current_timestamp(),
  `last_checked` datetime DEFAULT NULL,
  `retry_attempt` tinyint(3) NOT NULL DEFAULT 0,
  `last_updated` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`),
  KEY `rank` (`rank`),
  KEY `last_checked_index` (`last_checked`),
  KEY `ignorerow` (`retry_attempt`),
  KEY `last_updated` (`last_updated`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `index_page` (
  `rankdb_id` bigint(20) NOT NULL,
  `contents` blob DEFAULT NULL,
  `content_size` int(11) DEFAULT NULL,
  `headers` varchar(1000) DEFAULT NULL,
  `cert_issuer` char(100) DEFAULT NULL,
  `cert_expiry` datetime DEFAULT NULL,
  `last_updated` datetime NOT NULL DEFAULT current_timestamp(),
  `title` char(255) DEFAULT NULL,
  PRIMARY KEY (`rankdb_id`),
  KEY `cert_issuer` (`cert_issuer`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `kv_store` (
  `rankdb_id` bigint(20) NOT NULL,
  `row_key` char(10) NOT NULL,
  `row_value` varchar(100) NOT NULL,
  `last_update` datetime NOT NULL DEFAULT current_timestamp(),
  KEY `rankdb_id` (`rankdb_id`),
  KEY `row_key` (`row_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
