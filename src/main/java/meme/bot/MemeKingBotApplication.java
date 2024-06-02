package meme.bot;

import discord4j.core.DiscordClientBuilder;
import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.EventDispatcher;
import discord4j.core.event.domain.message.MessageCreateEvent;
import discord4j.rest.RestClient;
import meme.bot.service.MessageService;
import meme.bot.utils.MessageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.annotation.Bean;

import java.util.List;

@SpringBootApplication
@EnableAutoConfiguration
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
			MessageInfo info = new MessageInfo(event);
			if (listeningChannels.contains(info.getChannelId())) {
				messageService.processMessage(info);
			}
		});
		return client;
	}

	@Bean
	public RestClient discordRestClient(GatewayDiscordClient client) {
		return client.getRestClient();
	}



}
