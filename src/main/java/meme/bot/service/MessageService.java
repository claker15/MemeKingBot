package meme.bot.service;

import com.austinv11.servicer.Service;
import dev.brachtendorf.jimagehash.hash.Hash;
import dev.brachtendorf.jimagehash.hashAlgorithms.HashingAlgorithm;
import dev.brachtendorf.jimagehash.hashAlgorithms.PerceptiveHash;
import discord4j.core.object.entity.Attachment;
import discord4j.core.object.entity.Message;
import discord4j.discordjson.json.AttachmentData;
import meme.bot.domain.subclasses.Post;
import meme.bot.repository.PostRepository;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.net.URI;
import java.util.List;

@Service
public class MessageService {

    @Autowired
    private PostRepository postRepository;

    public void processMessage(Message message) {

        System.out.println("Got message");
        List<Attachment> attachments =  message.getAttachments();
        attachments.forEach(attachment -> {
            try {
                Hash newHash = hashImage(attachment);
                Boolean exists = hashExists(newHash);
                if (!exists) {
                    //add new post and award points
                }
                else {
                    //send cringe message
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
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

    private Boolean hashExists(Hash hash) {
        Post existingHash = postRepository.findByHash(hash.toString());
        return existingHash != null;
    }

}
