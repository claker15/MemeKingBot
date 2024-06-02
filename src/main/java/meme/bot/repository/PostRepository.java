package meme.bot.repository;

import meme.bot.domain.subclasses.Post;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.math.BigInteger;
import java.time.LocalDate;
import java.util.Date;
import java.util.List;

public interface PostRepository extends JpaRepository<Post, Long> {

    Post findByHash(BigInteger hash);

    List<Post> findByUserIdAndGuildIdAndCreatedAfterOrderByCreatedDesc(String userId, String guildId, Date date);

    @Query(value = "select rand(), user_id from post where guild_id = :guild AND WEEK(created) = WEEK(NOW()) - 1 ORDER BY RAND()", nativeQuery = true)
    String getRandUserId(@Param(value="guild")String guildId);

}
