# vds-tts-dev-consumer — Workflow

Generate a Kafka consumer setup for Spring Boot, following the **updated VDS/Viettel stack pattern**:
- Config class **extends `KafkaBaseConfig`** and calls `super.buildContainerFactory(...)`
- Listener class is a `@Service` in `service/kafka/` package

---

## STEP 1 — COLLECT INPUTS

If arguments were passed, parse them. Otherwise ask the user for all required fields in one message:

| Field | Example | Description |
|---|---|---|
| `ConsumerName` | `ReconcileReceive` | PascalCase name (becomes config class prefix) |
| `basePackage` | `com.example.app` | Root Java package of the project |
| `propertyPrefix` | `spring.kafka.receive.reconcile` | Config property namespace |
| `messageType` | `ReconcileDataDifference` | Java class to deserialize the Kafka message into (short name) |

Derive automatically:
- `consumerNameLower` = camelCase of `ConsumerName` (e.g. `reconcileReceive`)
- `configClassName` = `Kafka{ConsumerName}ConsumerConfig`
- `containerFactoryBeanName` = `kafka{ConsumerName}ContainerFactory`
- `listenerClassName` = `{ConsumerName}Consumer`
- `consumerTopicPrefix` = `spring.kafka.consumer.` + the part of `propertyPrefix` after `spring.kafka.`
  - Example: `propertyPrefix=spring.kafka.receive.reconcile` → `consumerTopicPrefix=spring.kafka.consumer.receive.reconcile`
  - Example: `propertyPrefix=spring.kafka.information` → `consumerTopicPrefix=spring.kafka.consumer.information`

---

## STEP 2 — CHECK EXISTING FILES

Before generating, scan the project for:

1. `KafkaBaseConfig.java` at `src/main/java/{basePackagePath}/config/kafka/KafkaBaseConfig.java`
   - **Must exist** — if not found, halt and instruct the user to run the producer skill first (it creates `KafkaBaseConfig`)
2. `config/kafka/consumer/{configClassName}.java` — halt and ask if found
3. `service/kafka/{listenerClassName}.java` — halt and ask if found

---

## STEP 3 — GENERATE FILES

### File 1 — `{configClassName}.java`

Path: `config/kafka/consumer/{configClassName}.java`

```java
package {basePackage}.config.kafka.consumer;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import {basePackage}.config.kafka.KafkaBaseConfig;

@Configuration
@RequiredArgsConstructor
@Slf4j
@ConditionalOnProperty(
        value = "{propertyPrefix}.enabled",
        matchIfMissing = false,
        havingValue = "true"
)
@EnableKafka
public class {configClassName} extends KafkaBaseConfig {

    @Value("${{{propertyPrefix}.bootstrap-servers}}")
    private String bootstrapServers;

    @Value("${{{propertyPrefix}.security.protocol}}")
    private String protocol;

    @Value("${{{propertyPrefix}.username}}")
    private String username;

    @Value("${{{propertyPrefix}.password}}")
    private String password;

    @Value("${{{propertyPrefix}.concurrency}}")
    private Integer concurrency;

    @Bean("{containerFactoryBeanName}")
    public ConcurrentKafkaListenerContainerFactory<String, String> {containerFactoryBeanName}() {
        log.info("Init {containerFactoryBeanName}");
        return super.buildContainerFactory(bootstrapServers, username, password, protocol, concurrency);
    }
}
```

---

### File 2 — `{listenerClassName}.java`

Path: `service/kafka/{listenerClassName}.java`

```java
package {basePackage}.service.kafka;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;
import {basePackage}.config.AppConfig;
import {basePackage}.dto.{messageType};

@Service
@Slf4j
public class {listenerClassName} {

    @Autowired
    private AppConfig appConfig;

    @KafkaListener(
            containerFactory = "{containerFactoryBeanName}",
            topics = "${{{consumerTopicPrefix}.topic-name}}",
            groupId = "${{{consumerTopicPrefix}.group-id}}",
            autoStartup = "${{{propertyPrefix}.auto-startup}}")
    public void consume(
            @Payload String message,
            @Header(KafkaHeaders.RECEIVED_PARTITION_ID) int partitionId,
            @Header(KafkaHeaders.OFFSET) String offset) {
        log.info("Received message partition [{}] offset [{}]: {}", partitionId, offset, message);
        try {
            {messageType} payload = appConfig.objectMapper().readValue(message, {messageType}.class);
            log.info("Parsed payload: {}", payload);
            // TODO: implement business logic here
        } catch (com.fasterxml.jackson.core.JsonProcessingException e) {
            log.error("Error parsing message: {}", message, e);
        } catch (Exception e) {
            log.error("Unexpected error processing message", e);
        }
    }
}
```

> **Note:** If `AppConfig` does not exist in the project, replace `appConfig.objectMapper().readValue(...)` with `new com.fasterxml.jackson.databind.ObjectMapper().readValue(...)` or inject `ObjectMapper` directly as a bean.

---

### File 3 — `application.properties` snippet

```properties
{propertyPrefix}.enabled=true
{propertyPrefix}.bootstrap-servers=kafka-1:9092,kafka-2:9092,kafka-3:9092
{propertyPrefix}.security.protocol=SASL_PLAINTEXT
# Leave blank to disable SASL:
{propertyPrefix}.username=
{propertyPrefix}.password=
{propertyPrefix}.concurrency=1
{propertyPrefix}.auto-startup=true

# Consumer-specific (used in @KafkaListener):
{consumerTopicPrefix}.topic-name=YOUR_TOPIC_NAME
{consumerTopicPrefix}.group-id=YOUR_CONSUMER_GROUP_ID
```

---

## STEP 4 — PRESENT RESULTS

Show:
1. Files created / skipped (with relative paths)
2. The `application.properties` snippet
3. TODOs:
   - Implement business logic inside `// TODO` in `{listenerClassName}`
   - Inject any dependencies needed for business logic (repositories, services, producers)
   - Verify `{messageType}` DTO exists; if not, create it in `dto/`
4. Usage note — the listener activates automatically via `@ConditionalOnProperty` + `autoStartup`
