package meme.bot.MemeKingBot;

import discord4j.core.DiscordClient;
import discord4j.core.DiscordClientBuilder;
import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.EventDispatcher;
import discord4j.core.event.domain.message.MessageCreateEvent;
import discord4j.core.object.entity.Message;
import discord4j.core.object.presence.ClientActivity;
import discord4j.core.object.presence.ClientPresence;
import discord4j.rest.RestClient;
import meme.bot.service.MessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;

import java.util.List;

@SpringBootApplication
@ComponentScan(basePackageClasses = {meme.bot.MemeKingBot.GlobalCommandRegistrar.class})
public class MemeKingBotApplication {

	@Value("${bot.token}")
	private String botToken;

	@Value("#{'${bot.channels.messages}'.split(',')}")
	private List<String> listeningChannels;

	@Autowired
	private MessageService messageService;

	public static void main(String[] args) {
		//Start spring application
		new SpringApplicationBuilder(MemeKingBotApplication.class)
				.build()
				.run(args);
	}


	@Bean
	public GatewayDiscordClient gatewayDiscordClient() {
		GatewayDiscordClient client =  DiscordClientBuilder.create(botToken)
				.build()
				.gateway()
				.setEventDispatcher(EventDispatcher.replaying())
				.login()
				.block();

		//register regular message listener
		client.on(MessageCreateEvent.class).subscribe(event -> {
			Message message = event.getMessage();
			if (listeningChannels.contains(message.getChannel().block().getId().asString())) {
				messageService.processMessage(message);
			}
		});
		return client;
	}

	@Bean
	public RestClient discordRestClient(GatewayDiscordClient client) {
		return client.getRestClient();
	}

}
