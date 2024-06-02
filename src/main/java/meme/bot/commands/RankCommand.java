package meme.bot.commands;

import discord4j.core.event.domain.interaction.ChatInputInteractionEvent;
import meme.bot.factory.RankingEmbedFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

@Component
public class RankCommand implements SlashCommand{

    @Autowired
    private RankingEmbedFactory rankingEmbedFactory;

    @Override
    public String getName() {
        return "ranking";
    }

    @Override
    public Mono<Void> handle(ChatInputInteractionEvent event) {
        return event.reply()
                .withEmbeds(rankingEmbedFactory.buildRankingMessage("ranking", event.getInteraction().getGuildId().get().asString()));
    }
}
