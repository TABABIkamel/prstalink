package com.aoservice.beans;

import com.aoservice.entities.AppelOffre;
import com.aoservice.entities.CandidatureFinished;
import com.aoservice.entities.Notification;
import com.aoservice.repositories.AppellOffreRepository;
import com.aoservice.repositories.NotificationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.messaging.simp.SimpMessageType;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

@Component
public class AoWorkflowBean {
    @Autowired
    AppellOffreRepository appellOffreRepository;
    @Autowired
    NotificationRepository notificationRepository;
    @Autowired
    AppelOffreBean appelOffreBean;

    public void notificationForSubmitReview(Optional<CandidatureFinished> candidatureFinished, Set<String> listeners, SimpMessagingTemplate template) {
        if (candidatureFinished.isPresent()) {
            var notification = new Notification();
            Optional<AppelOffre> appelOffre = Optional.ofNullable(appellOffreRepository.findByRefAo(candidatureFinished.get().getRefAo()));
            for (String listener : listeners) {
                var headerAccessor = SimpMessageHeaderAccessor.create(SimpMessageType.MESSAGE);
                headerAccessor.setSessionId(listener);
                headerAccessor.setLeaveMutable(true);
                if (appelOffre.isPresent()) {
                    template.convertAndSendToUser(
                            listener,
                            "/notification/item" + candidatureFinished.get().getUsername(),
                            appelOffre.get().getEsn().getEsnnom() + " a examiné votre candidature pour l appel offre " + appelOffre.get().getTitreAo(),
                            headerAccessor.getMessageHeaders());
                    // send notification par mail
                    Map<String, Object> model = new HashMap<>();
                    model.put("nameEsn",appelOffre.get().getEsn().getEsnnom());
                    model.put("titreAo",appelOffre.get().getTitreAo());
                    appelOffreBean.sendMail(appelOffre.get().getEsn().getEsnEmail(),model,"Notification À propos votre candidature "+appelOffre.get().getTitreAo(),"mail-notification-prestataire");

                    //store notification in database
                    notification.setContent(appelOffre.get().getEsn().getEsnnom() + " a examiné votre candidature pour l appel offre " + appelOffre.get().getTitreAo());
                    notification.setUsernameSender(appelOffre.get().getEsn().getEsnnom());
                    notification.setUsernameReceiver(candidatureFinished.get().getUsername());
                    notification.setUrlImageReceiver(appelOffre.get().getEsn().getLocationImage());
                    notificationRepository.save(notification);
                }
            }
        }
    }
}
