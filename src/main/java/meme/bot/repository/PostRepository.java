package meme.bot.repository;

import meme.bot.domain.subclasses.Post;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;
import java.util.Date;
import java.util.List;

public interface PostRepository extends JpaRepository<Post, Long> {

    Post findByHash(String hash);

    List<Post> findByUserIdAndGuildIdAndCreatedAfterOrderByCreatedDesc(String userId, String guildId, Date date);

    @Query("select DISTINCT userId from post where guildId = ?1 AND YEARWEEK(created) = YEARWEEK(NOW() - INTERVAL 1 WEEK) ORDER BY RAND()")
    String getRandUserId(String guildId);

}
