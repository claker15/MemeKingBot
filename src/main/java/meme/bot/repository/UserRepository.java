package meme.bot.repository;

import meme.bot.domain.subclasses.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface UserRepository extends JpaRepository<User, Long> {

    @Query(value = "SELECT user_id, SUM(point_value) as count FROM Points WHERE guild_id = :guild AND WEEK(created) = WEEK(NOW()) GROUP BY user_id ORDER BY SUM(point_value) DESC LIMIT 5", nativeQuery = true)
    List<Object[]> getWeeklyUserRankings(@Param(value="guild")String guildId);

}
