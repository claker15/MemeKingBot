package meme.bot.repository;

import meme.bot.domain.subclasses.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface UserRepository extends JpaRepository<User, Long> {

    @Query("SELECT userId, SUM(pointValue) as count FROM Point WHERE guildId = :guild AND YEARWEEK(created) = YEARWEEK(NOW()) GROUP BY userId ORDER BY SUM(pointValue) DESC LIMIT 5")
    List<User> getWeeklyUserRankings(@Param(value="guild")String guildId);

}
