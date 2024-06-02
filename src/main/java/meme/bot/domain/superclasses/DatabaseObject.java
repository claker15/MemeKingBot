package meme.bot.domain.superclasses;


import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import org.springframework.cglib.core.Local;

import java.time.LocalDate;
import java.util.Date;

@MappedSuperclass
public class DatabaseObject {

    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)
    private Long id;
    private Date created;
    private String userId;
    private String guildId;


    public DatabaseObject(String userId, String guildId) {

        this.userId = userId;
        this.guildId = guildId;
        this.created = new Date();

    }

    public DatabaseObject() {

    }

    public Long getId() {
        return id;
    }

    public Date getCreated() {
        return created;
    }

    public String getUserId() {
        return userId;
    }

    public String getGuildId() {
        return guildId;
    }
}
