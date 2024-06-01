package meme.bot.service;

import com.austinv11.servicer.Service;
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
import meme.bot.utils.MessageInfo;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.util.Date;
import java.util.List;

@Service
public class MessageService {

    @Autowired
    private PostRepository postRepository;

    @Autowired
    private PointRepository pointRepository;

    @Value("${bot.cooldown.durationInSecs}")
    private Integer cooldownThreshold;

    public void processMessage(MessageInfo messageInfo) {

        System.out.println("Got message");

        //need to get both attachments and urls
        //url examples: https://github.com/robinst/autolink-java
        List<Attachment> attachments =  messageInfo.getMessage().getAttachments();
        attachments.forEach(attachment -> {
            Hash newHash;
            try {
                newHash = hashImage(attachment);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            Post post = hashExists(newHash);
            if (post == null) {
                createPost(messageInfo.getAuthorId(), messageInfo.getGuildId(), newHash.toString(), messageInfo.getMessageId());
                String newUserId = postRepository.getRandUserId(messageInfo.getGuildId());
                if (onCooldown(messageInfo.getAuthorId(), messageInfo.getGuildId())) {
                    createPostPoints(newUserId, messageInfo.getGuildId(), messageInfo.getMessageId(), messageInfo.getAuthorId());
                    messageInfo.getMessage().getChannel()
                            .flatMap(channel -> channel.createMessage(ResponseMessageFactory.buildResponseMessage("relax", messageInfo.getAuthorId(), newUserId)));
                }
                else {
                    createPostPoints(messageInfo.getAuthorId(), messageInfo.getGuildId(), messageInfo.getMessageId(), null);
                }
            }
            else {
                //send cringe message
                messageInfo.getMessage().getChannel()
                        .flatMap(channel -> channel.createMessage(ResponseMessageFactory.buildResponseMessage("cringe", messageInfo.getAuthorId(), post.getCreated().toString(), post.getUserId())));
            }
        });
    }

    private Hash hashImage(Attachment attachment) throws IOException {

        AttachmentData data = attachment.getData();
        String imageUrl = data.url();
        File newFile = new File("");
        try {
            FileUtils.copyURLToFile(URI.create(imageUrl).toURL(), newFile);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        HashingAlgorithm hasher = new PerceptiveHash(16);
        return hasher.hash(newFile);
    }

    private Post hashExists(Hash hash) {
        return postRepository.findByHash(hash.toString());
    }

    private void createPost(String userId, String guildId, String hash, String messageId) {
        Post post = new Post(userId, guildId, hash, messageId);
        postRepository.save(post);
    }
    private void createPostPoints(String userId, String guildId, String messageId, String userIdFrom) {
        Point point = new Point(userId, guildId, 1, "POST", userIdFrom, messageId);
        pointRepository.save(point);
    }
    private Boolean onCooldown(String userId, String guildId) {
        List<Post> posts = postRepository.findByUserIdAndGuildIdAndCreatedAfterOrderByCreatedDesc(userId, guildId, new Date(System.currentTimeMillis() - (1000L * cooldownThreshold)));
        return !posts.isEmpty();
    }

}
