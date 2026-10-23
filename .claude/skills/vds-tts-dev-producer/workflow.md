# vds-tts-dev-producer — Workflow

Generate a complete Kafka producer setup for Spring Boot, following the VDS/Viettel stack pattern.

---

## STEP 1 — COLLECT INPUTS

If arguments were passed (e.g. `/vds-tts-dev-producer NotificationEvent com.example.app`), parse them.
Otherwise ask the user for all required fields in one message:

| Field | Example | Description |
|---|---|---|
| `ProducerName` | `NotificationEvent` | PascalCase name (becomes bean prefix) |
| `basePackage` | `com.example.app` | Root Java package of the project |
| `propertyPrefix` | `spring.kafka.notification` | Config property namespace in application.yml |
| `topicPropertyKey` | `notification.event.topic` | Property key for the Kafka topic |
| `dtoClass` | `NotificationEventDTO` | DTO class to publish (short name) |
| `partitionKeyField` | `getId()` | Field on DTO used as Kafka message key |

Derive automatically:
- `producerNameLower` = camelCase of `ProducerName` (e.g. `notificationEvent`)
- `configBeanName` = `{producerNameLower}ProducerFactory`
- `templateBeanName` = `{producerNameLower}KafkaTemplate`
- `containerFactoryQualifier` = `@Qualifier("{templateBeanName}")`

---

## STEP 2 — CHECK EXISTING FILES

Before generating, scan the project for:

1. `KafkaBaseConfig.java` — search under `src/main/java/{basePackage path}/config/kafka/producer/config/`
2. `KafkaBaseProducer.java` — search under `src/main/java/{basePackage path}/config/kafka/producer/impl/`

For each found file: **skip generation, reuse as-is.** Inform the user which base files were reused.

---

## STEP 3 — GENERATE FILES

Generate only the files that do not already exist. Place all files under `src/main/java/{basePackagePath}/`.

### File 1 — `KafkaBaseConfig.java` (skip if exists)

Path: `config/kafka/producer/config/KafkaBaseConfig.java`

```java
package {basePackage}.config.kafka.producer.config;

import org.apache.commons.lang3.StringUtils;
import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.security.plain.PlainLoginModule;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.serializer.JsonSerializer;

import java.util.HashMap;
import java.util.Map;

public class KafkaBaseConfig {

    public ProducerFactory<String, Object> buildProducerFactory(
            String kafkaServers,
            String retries,
            String requestTimeout,
            String username,
            String password,
            String securityProtocol) {

        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        props.put(ProducerConfig.REQUEST_TIMEOUT_MS_CONFIG, requestTimeout);
        props.put(ProducerConfig.RETRIES_CONFIG, retries);
        if (StringUtils.isNotBlank(username) && StringUtils.isNotBlank(password)) {
            props.put(SaslConfigs.SASL_MECHANISM, "PLAIN");
            props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, securityProtocol);
            props.put(SaslConfigs.SASL_JAAS_CONFIG,
                    String.format("%s required username=\"%s\" password=\"%s\";",
                            PlainLoginModule.class.getName(), username, password));
        }
        return new DefaultKafkaProducerFactory<>(props, new StringSerializer(), new JsonSerializer<>());
    }
}
```

---

### File 2 — `KafkaBaseProducer.java` (skip if exists)

Path: `config/kafka/producer/impl/KafkaBaseProducer.java`

```java
package {basePackage}.config.kafka.producer.impl;

import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.util.concurrent.ListenableFutureCallback;

@Service
@Slf4j
public class KafkaBaseProducer {

    public void sendMessage(String topic, String key, Object payload, KafkaTemplate<String, Object> kafkaTemplate) {
        ListenableFuture<SendResult<String, Object>> future = kafkaTemplate.send(topic, key, payload);
        future.addCallback(new ListenableFutureCallback<>() {
            @Override
            public void onFailure(@NotNull Throwable ex) {
                log.error("Failed to send message to topic [{}]: {}", topic, ex.getMessage());
            }

            @Override
            public void onSuccess(SendResult<String, Object> result) {
                log.info("Sent message to topic [{}] at offset [{}]",
                        topic, result.getRecordMetadata().offset());
            }
        });
    }
}
```

> Note: If the project uses Spring Boot 3.x / Spring Kafka 3.x, replace `ListenableFuture` with `CompletableFuture` and use `.whenComplete()` instead of `.addCallback()`.

---

### File 3 — `{ProducerName}ProducerConfig.java`

Path: `config/kafka/producer/config/impl/{ProducerName}ProducerConfig.java`

```java
package {basePackage}.config.kafka.producer.config.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import {basePackage}.config.kafka.producer.config.KafkaBaseConfig;

@Configuration
@RequiredArgsConstructor
@ConditionalOnProperty(value = "{propertyPrefix}.enabled", havingValue = "true")
public class {ProducerName}ProducerConfig extends KafkaBaseConfig {

    @Value("${{{propertyPrefix}.bootstrap-servers}}")
    private String bootstrapServers;

    @Value("${{{propertyPrefix}.security.protocol}}")
    private String securityProtocol;

    @Value("${{{propertyPrefix}.username}}")
    private String username;

    @Value("${{{propertyPrefix}.password}}")
    private String password;

    @Value("${{{propertyPrefix}.retries:3}}")
    private String retries;

    @Value("${{{propertyPrefix}.request-timeout:30000}}")
    private String requestTimeout;

    @Bean("{configBeanName}")
    public ProducerFactory<String, Object> {configBeanName}() {
        return super.buildProducerFactory(bootstrapServers, retries, requestTimeout, username, password, securityProtocol);
    }

    @Bean("{templateBeanName}")
    public KafkaTemplate<String, Object> {templateBeanName}() {
        return new KafkaTemplate<>({configBeanName}());
    }
}
```

---

### File 4 — `{ProducerName}Producer.java`

Path: `config/kafka/producer/impl/{ProducerName}Producer.java`

```java
package {basePackage}.config.kafka.producer.impl;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import {basePackage}.dto.{dtoClass};

import java.util.concurrent.CompletableFuture;

@Service
@Slf4j
public class {ProducerName}Producer extends KafkaBaseProducer {

    @Autowired
    @Qualifier("{templateBeanName}")
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Value("${{{topicPropertyKey}}}")
    private String topic;

    public void push({dtoClass} dto) {
        CompletableFuture.runAsync(() -> {
            try {
                log.info("Pushing {ProducerName} message: {}", dto);
                String key = String.valueOf(dto.{partitionKeyField});
                super.sendMessage(topic, key, dto, kafkaTemplate);
            } catch (Exception e) {
                log.error("Failed to push {ProducerName} message", e);
            }
        });
    }
}
```

---

### File 5 — `application.properties` snippet

Output as a code block for the user to merge manually:

```properties
{propertyPrefix}.enabled=true
{propertyPrefix}.bootstrap-servers=localhost:9092
{propertyPrefix}.security.protocol=PLAINTEXT
# Leave blank to disable SASL:
{propertyPrefix}.username=
{propertyPrefix}.password=
{propertyPrefix}.retries=3
{propertyPrefix}.request-timeout=30000

{topicPropertyKey}=your-topic-name
```

---

## STEP 4 — PRESENT RESULTS

Show:
1. List of files created / skipped (with relative paths)
2. The application.properties snippet
3. A usage example showing how to inject and call the producer

Example usage block:
```java
@Autowired
private {ProducerName}Producer {producerNameLower}Producer;

// In your service method:
{producerNameLower}Producer.push(dto);
```
