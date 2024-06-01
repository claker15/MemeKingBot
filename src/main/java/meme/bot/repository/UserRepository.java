package meme.bot.repository;

import meme.bot.domain.subclasses.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface UserRepository extends JpaRepository<User, Long> {

    @Query("SELECT userId, SUM(value) as count FROM point WHERE guild_id = ?0 AND YEARWEEK(created) = YEARWEEK(NOW()) GROUP BY user_id ORDER BY SUM(value) DESC LIMIT 5")
    List<User> getWeeklyUserRankings(String guildId);

}
