package com.aoservice.service;

import com.aoservice.configurationMapper.EsnMapper;
import com.aoservice.configurationMapper.PrestataireMapper;
import com.aoservice.dto.EducationDto;
import com.aoservice.dto.EsnDto;
import com.aoservice.dto.ExperienceDto;
import com.aoservice.dto.PrestataireDto;
import com.aoservice.entities.Education;
import com.aoservice.entities.Esn;
import com.aoservice.entities.Experience;
import com.aoservice.entities.Prestataire;
import com.aoservice.repositories.EducationRepository;
import com.aoservice.repositories.EsnRepository;
import com.aoservice.repositories.ExperienceRepository;
import com.aoservice.repositories.PrestataireRepository;
import com.cloudinary.Cloudinary;
import com.cloudinary.utils.ObjectUtils;
import org.apache.log4j.Logger;
import org.mapstruct.factory.Mappers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.attribute.FileAttribute;
import java.nio.file.attribute.PosixFilePermission;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class CompleteProfileService {
    @Autowired
    EsnRepository esnRepository;
    @Autowired
    private PrestataireRepository prestataireRepository;
    @Autowired
    private EducationRepository educationRepository;
    @Autowired
    private ExperienceRepository experienceRepository;
    private PrestataireMapper mapperPrestataire = Mappers.getMapper(PrestataireMapper.class);
    private EsnMapper mapperEsn = Mappers.getMapper(EsnMapper.class);
    public static final Logger LOGGER = Logger.getLogger(CompleteProfileService.class);

    public ResponseEntity<EsnDto> completeProfileEsn(EsnDto esnDto,String username){
        Optional<Esn> esn = Optional.of(mapperEsn.esnDTOtoEsn(esnDto));
        if(esn.get()!=null){
            esn.get().setEsnUsernameRepresentant(username);
            esn.get().setEsnIsCompleted(true);
            esn.get().setEsnIsPrestataire(false);
            //esn.get().setLocationImage((String)uploadResult.get("url"));
            return new ResponseEntity<>(mapperEsn.esnToEsnDTO(esnRepository.save(esn.get())), HttpStatus.CREATED) ;
        }else
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
    }

    public ResponseEntity<String> setPhotoToEsn(MultipartFile file,String username) throws IOException {

        String fileName = file.getOriginalFilename();
        String prefix = fileName!=null?fileName.substring(fileName.lastIndexOf(".")):"";

        File file1 = new File("");
        try {
            //FileAttribute<Set<PosixFilePermission>> attr = PosixFilePermissions.asFileAttribute(PosixFilePermissions.fromString("w+"));
            //Files.createTempFile("prefix", "suffix", attr);
            file1 = File.createTempFile(fileName, prefix);
            file.transferTo(file1);
        } catch (Exception e) {
            LOGGER.info(e.getMessage());
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        } finally {
            File f = new File(file1.toURI());
        }
        Cloudinary cloudinary = new Cloudinary(ObjectUtils.asMap(
                "cloud_name", "dhum7apjy",
                "api_key", "265837847724928",
                "api_secret", "CVKzJr7cldr0au9oFSh6t3mGqzw"));
        //File file = new File("img1.png");
        Map uploadResult = cloudinary.uploader().upload(file1, ObjectUtils.emptyMap());
        System.out.println(uploadResult.get("url"));
        Esn esn=esnRepository.findByEsnUsernameRepresentant(username);
        Optional<Esn> esnOptional=Optional.ofNullable(esn);
        if(esnOptional.isPresent()){
            System.out.println("in if");
            esn.setLocationImage((String)uploadResult.get("url"));
            esnRepository.save(esn);
            return new ResponseEntity<>(HttpStatus.OK);
        }else
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
    }

    public ResponseEntity<String> setPhotoToPrestataire(MultipartFile file,String username) throws IOException {

        String fileName = file.getOriginalFilename();
        String prefix = fileName!=null?fileName.substring(fileName.lastIndexOf(".")):"";

        File file1 = new File("");
        try {
            file1 = File.createTempFile(fileName, prefix);
            file.transferTo(file1);
        } catch (Exception e) {
            LOGGER.info(e.getMessage());
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);

        } finally {
            // After operating the above files, you need to delete the temporary files generated in the root directory
            File f = new File(file1.toURI());
            // f.delete();
        }
        Cloudinary cloudinary = new Cloudinary(ObjectUtils.asMap(
                "cloud_name", "dhum7apjy",
                "api_key", "265837847724928",
                "api_secret", "CVKzJr7cldr0au9oFSh6t3mGqzw"));
        //File file = new File("img1.png");
        Optional<Prestataire> prestataire = Optional.ofNullable(prestataireRepository.findByPrestataireUsername(username));
        Map uploadResult = cloudinary.uploader().upload(file1, ObjectUtils.emptyMap());
        System.out.println(uploadResult.get("url"));
        if (prestataire.isPresent()) {
            System.out.println("in if");
            prestataire.get().setLocationImage((String) uploadResult.get("url"));
            prestataireRepository.save(prestataire.get());
            return new ResponseEntity<>(HttpStatus.OK);
        }else
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
    }

    public ResponseEntity<EsnDto> checkIfProfileEsnCompleted(String usename){
        Optional<Esn> esn = Optional.ofNullable(esnRepository.findByEsnUsernameRepresentant(usename));
        if(esn.isPresent()){
            return new ResponseEntity<>(mapperEsn.esnToEsnDTO(esn.get()),HttpStatus.OK);
        }else
            return new ResponseEntity<>(null,HttpStatus.NOT_FOUND);
    }

    public ResponseEntity<PrestataireDto> checkIfProfilePrestataireCompleted(String usename){
        Optional<Prestataire> prestataire = Optional.ofNullable(prestataireRepository.findByPrestataireUsername(usename));
        if (prestataire.isPresent())
            return new ResponseEntity<>(mapperPrestataire.prestataireToPrestataireDTO(prestataire.get()), HttpStatus.OK);
        else
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    public ResponseEntity<PrestataireDto> CompleterProfilPrestataire(PrestataireDto prestataireDto){
        Prestataire prestataire = mapperPrestataire.prestataireDTOToPrestataire(prestataireDto);
        List<Education> educations = prestataireDto.getEducation().stream().map(educationDto -> mapperPrestataire.educationDtoToEducation(educationDto)).collect(Collectors.toList());
        List<Experience> experiences = prestataireDto.getExperience().stream().map(experienceDto -> mapperPrestataire.experienceDtoToExperience(experienceDto)).collect(Collectors.toList());
        if (prestataire != null) {
            if (prestataireRepository.findByPrestataireUsername(prestataire.getPrestataireUsername()) != null) {
                return new ResponseEntity<>(HttpStatus.FOUND);
            }
            prestataire.setPrestataireIsCompleted(true);

            for (Education education : educations)
                education.setPrestataire(prestataire);

            for (Experience experience : experiences)
                experience.setPrestataire(prestataire);
            prestataire.setPrestataireEducation(educations);
            prestataire.setPrestataireExperience(experiences);
            prestataireRepository.save(prestataire);
            return new ResponseEntity<>(prestataireDto, HttpStatus.CREATED);
        } else
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
    }

    public ResponseEntity<PrestataireDto> getPrestataireByUsername(String username) {
        Optional<Prestataire> prestataire=Optional.ofNullable(prestataireRepository.findByPrestataireUsername(username));
        if (prestataire.isPresent()){
            return new ResponseEntity<>(mapperPrestataire.prestataireToPrestataireDTO(prestataire.get()),HttpStatus.OK);
        }
        else
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    public ResponseEntity<EsnDto> getEsnByUsername(String username) {
        Optional<Esn> esn=Optional.ofNullable(esnRepository.findByEsnUsernameRepresentant(username));
        if (esn.isPresent()){
            return new ResponseEntity<>(mapperEsn.esnToEsnDTO(esn.get()),HttpStatus.OK);
        }
        else
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    public ResponseEntity<String> modifierPrestataireProfile(PrestataireDto prestataireDto) {
        if(prestataireDto!=null){
            prestataireRepository.save(mapperPrestataire.prestataireDTOToPrestataire(prestataireDto));
            return new ResponseEntity<>("profile modifié",HttpStatus.OK);
        }else
            return new ResponseEntity<>("profile non modifié",HttpStatus.BAD_REQUEST);
    }

    public ResponseEntity<String> modifierESnProfile(EsnDto esnDto) {
        if(esnDto!=null){
            esnRepository.save(mapperEsn.esnDTOtoEsn(esnDto));
            return new ResponseEntity<>("profile modifié",HttpStatus.OK);
        }else
            return new ResponseEntity<>("profile non modifié",HttpStatus.BAD_REQUEST);
    }
    public ResponseEntity<PrestataireDto> getPrestataireWithHisCvByUsername(String username) {
        Optional<Prestataire> prestataire=Optional.ofNullable(prestataireRepository.findByPrestataireUsername(username));
        if (prestataire.isPresent()){
//            List<Education> educations=educationRepository.findAll().stream().filter(education -> Objects.equals(education.getPrestataire().getPrestataireId(), prestataire.get().getPrestataireId())).collect(Collectors.toList());
//            List<Experience> experiences=experienceRepository.
            PrestataireDto prestataireDto=mapperPrestataire.prestataireToPrestataireDTO(prestataire.get());
            List<EducationDto> educationsDto=prestataire.get().getPrestataireEducation().stream().map(education -> mapperPrestataire.educationToEducationDTO(education)).collect(Collectors.toList());
            List<ExperienceDto> experiencesDto = prestataire.get().getPrestataireExperience().stream().map(experience -> mapperPrestataire.experienceToExperienceDTO(experience)).collect(Collectors.toList());
            prestataireDto.setEducation(educationsDto);
            prestataireDto.setExperience(experiencesDto);
            return new ResponseEntity<>(prestataireDto,HttpStatus.OK);
        }
        else
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    public ResponseEntity<PrestataireDto> modifierCvPrestataire(PrestataireDto prestataireDto){
        Prestataire prestataire = mapperPrestataire.prestataireDTOToPrestataire(prestataireDto);
        List<Education> educations = prestataireDto.getEducation().stream().map(educationDto -> mapperPrestataire.educationDtoToEducation(educationDto)).collect(Collectors.toList());
        List<Experience> experiences = prestataireDto.getExperience().stream().map(experienceDto -> mapperPrestataire.experienceDtoToExperience(experienceDto)).collect(Collectors.toList());
        if (prestataire != null) {
            for (Education education : educations)
                education.setPrestataire(prestataire);

            for (Experience experience : experiences)
                experience.setPrestataire(prestataire);
            prestataire.setPrestataireEducation(educations);
            prestataire.setPrestataireExperience(experiences);
            prestataireRepository.save(prestataire);
            return new ResponseEntity<>(prestataireDto, HttpStatus.CREATED);
        } else
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
    }
}
