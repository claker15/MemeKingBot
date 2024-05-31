package meme.bot.repository;

import meme.bot.domain.subclasses.Post;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PostRepository extends JpaRepository<Post, Long> {

    Post findByHash(String hash);

}
