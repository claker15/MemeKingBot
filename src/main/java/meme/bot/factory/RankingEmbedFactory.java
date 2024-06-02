package meme.bot.factory;

import discord4j.common.util.Snowflake;
import discord4j.core.DiscordClient;
import discord4j.core.GatewayDiscordClient;
import discord4j.core.object.entity.Member;
import discord4j.core.spec.EmbedCreateSpec;
import discord4j.core.spec.MessageCreateFields;
import discord4j.core.spec.MessageCreateSpec;
import discord4j.rest.util.Color;
import meme.bot.domain.subclasses.User;
import meme.bot.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import reactor.util.function.Tuple2;

import javax.imageio.ImageIO;
import java.util.ArrayList;
import java.util.List;

@Component
public class RankingEmbedFactory {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    GatewayDiscordClient gatewayDiscordClient;

    public EmbedCreateSpec buildRankingMessage(String type, String ...args) {

        EmbedCreateSpec.Builder embedSpec = EmbedCreateSpec.builder();

        List<Object[]> users = new ArrayList<>();
        switch (type) {
            case "ranking":
                users = userRepository.getWeeklyUserRankings(args[0]);
                embedSpec.title("Current Meme King Rankings");
                embedSpec.color(Color.BLUE);
                break;

            default:
                embedSpec.title("default value");
        }
        users.forEach(user -> {
            Member userNick = gatewayDiscordClient.getMemberById(Snowflake.of(args[0]), Snowflake.of(user[0].toString())).block();
            embedSpec.addField(userNick.getDisplayName(), user[1].toString(), false);
        });
        return embedSpec.build();

    }


}
