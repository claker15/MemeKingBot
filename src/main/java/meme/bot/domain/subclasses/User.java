package meme.bot.domain.subclasses;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import meme.bot.domain.superclasses.DatabaseObject;

@Entity
@Table(name = "users")
public class User extends DatabaseObject {
}
