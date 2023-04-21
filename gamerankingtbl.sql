CREATE TABLE GameRankingTbl 
    (
        GR_NO    INT(11) NOT NULL AUTO_INCREMENT,
        GR_NAME  VARCHAR(100) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
        GR_SCORE INT(11) NULL DEFAULT NULL,
        GR_DATE  DATETIME NULL DEFAULT current_timestamp(),
        PRIMARY KEY (`GR_NO`) USING BTREE
    )
    COMMENT='슈팅게임 게임순위 테이블'
    COLLATE='utf8mb4_general_ci'
    ENGINE=InnoDB
    ;gamerankingtbl