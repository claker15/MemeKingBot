package meme.bot.repository;

import meme.bot.domain.subclasses.Point;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PointRepository extends JpaRepository<Point, Long> {
}
