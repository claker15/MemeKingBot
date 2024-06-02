package meme.bot.service;

import dev.brachtendorf.jimagehash.hash.Hash;
import dev.brachtendorf.jimagehash.hashAlgorithms.HashingAlgorithm;
import dev.brachtendorf.jimagehash.hashAlgorithms.PerceptiveHash;
import discord4j.core.object.entity.Attachment;
import discord4j.discordjson.json.AttachmentData;
import meme.bot.domain.subclasses.Point;
import meme.bot.domain.subclasses.Post;
import meme.bot.factory.ResponseMessageFactory;
import meme.bot.repository.PointRepository;
import meme.bot.repository.PostRepository;
import meme.bot.utils.DateUtils;
import meme.bot.utils.MessageInfo;
import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.math.BigInteger;
import java.net.URI;
import java.util.Date;
import java.util.List;

@Service
public class MessageService {

    private final Logger LOGGER = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private PostRepository postRepository;

    @Autowired
    private PointRepository pointRepository;

    @Value("${bot.cooldown.durationInSecs}")
    private Integer cooldownThreshold;

    public void processMessage(MessageInfo messageInfo) {

        LOGGER.info("Received Message");

        //need to get both attachments and urls
        //url examples: https://github.com/robinst/autolink-java
        List<Attachment> attachments =  messageInfo.getMessage().getAttachments();
        LOGGER.info("found attachments for message id: {}", messageInfo.getMessageId());
        attachments.forEach(attachment -> {
            Hash newHash;
            try {
                newHash = hashImage(attachment);
                LOGGER.info("Calculated hash: {} for message id: {}", newHash.getHashValue(), messageInfo.getMessageId());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            Post post = hashExists(newHash);
            if (post == null) {
                LOGGER.info("Post is new, checking cooldown period for user: {}", messageInfo.getAuthorId());
                Boolean isCooldown = onCooldown(messageInfo.getAuthorId(), messageInfo.getGuildId());
                createPost(messageInfo.getAuthorId(), messageInfo.getGuildId(), newHash.getHashValue(), messageInfo.getMessageId());
                Post newUser = postRepository.getRandUserId(messageInfo.getGuildId(), DateUtils.getCurrentWeekBeginningAndEndDates().get(0), DateUtils.getCurrentWeekBeginningAndEndDates().get(1));
                if (isCooldown) {
                    LOGGER.info("User {} on cooldown, sending points to new user", messageInfo.getAuthorId());
                    createPostPoints(newUser.getUserId(), messageInfo.getGuildId(), messageInfo.getMessageId(), messageInfo.getAuthorId());
                    messageInfo.getMessage().getChannel()
                            .flatMap(channel -> channel.createMessage(ResponseMessageFactory.buildResponseMessage("relax", messageInfo.getAuthorId(), newUser.getUserId())))
                            .subscribe();
                }
                else {
                    createPostPoints(messageInfo.getAuthorId(), messageInfo.getGuildId(), messageInfo.getMessageId(), null);
                }
            }
            else {
                LOGGER.info("Post exists, sending cringe message for message id: {}", messageInfo.getMessageId());
                messageInfo.getMessage().getChannel()
                        .flatMap(channel -> channel.createMessage(ResponseMessageFactory.buildResponseMessage("cringe", messageInfo.getAuthorId(), post.getCreated().toString(), post.getUserId())))
                        .subscribe();
            }
        });
    }

    private Hash hashImage(Attachment attachment) throws IOException {

        AttachmentData data = attachment.getData();
        String imageUrl = data.url();
        File newFile = new File("/tmp/temp");
        try {
            FileUtils.copyURLToFile(URI.create(imageUrl).toURL(), newFile);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        HashingAlgorithm hasher = new PerceptiveHash(32);
        return hasher.hash(newFile);
    }

    private Post hashExists(Hash hash) {
        return postRepository.findByHash(hash.getHashValue());
    }

    private void createPost(String userId, String guildId, BigInteger hash, String messageId) {
        Post post = new Post(userId, guildId, hash, messageId);
        postRepository.save(post);
    }
    private void createPostPoints(String userId, String guildId, String messageId, String userIdFrom) {
        Point point = new Point(userId, guildId, 1, "POST", userIdFrom, messageId);
        pointRepository.save(point);
    }
    private Boolean onCooldown(String userId, String guildId) {
        List<Post> posts = postRepository.findByUserIdAndGuildIdAndCreatedAfterOrderByCreatedDesc(userId, guildId, new Date(System.currentTimeMillis() - (1000L * cooldownThreshold)));
        return posts != null && !posts.isEmpty();
    }

}
