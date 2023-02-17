CREATE TABLE `infos_rent` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_zone` int NOT NULL,
  `INSEE` int NOT NULL,
  `LIBGEO` varchar(256) NOT NULL,
  `DEP`  int NOT NULL,
  `REG` int NOT NULL,
  `TYPPRED` varchar(256) NOT NULL,
  `loypredm2` decimal NOT NULL,
  `lwr_IPm2` decimal NOT NULL,
  `upr_IPm2` decimal NOT NULL,
  `R2adj` decimal NOT NULL,
  `NBobs_maille` int NOT NULL,
  `NBobs_commune` int NOT NULL,
  PRIMARY KEY (`id`)
);
