/*
 * Copyright 2021 Jetperch LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @file
 *
 * @brief Port adapter for publish-subscribe.
 */

#ifndef FBP_COMM_PUBSUB_PORT_H_
#define FBP_COMM_PUBSUB_PORT_H_

#include "fitterbap/cmacro_inc.h"
#include "fitterbap/comm/transport.h"
#include "fitterbap/pubsub.h"
#include <stdint.h>
#include <stdbool.h>

/**
 * @ingroup fbp_comm
 * @defgroup fbp_comm_pubsub_port Publish-Subscribe Link over transport.
 *
 * @brief Provide a Publish-Subscribe Link over a transport port.
 *
 * This module provides a PubSub Link over the comm transport port protocol.
 * The Link provides reliable, distributed state recovery in the event
 * of connection loss or reset.
 *
 * @{
 */

FBP_CPP_GUARD_START

/// Default transmit timeout
#define FBP_PUBSUBP_TIMEOUT_MS  (250)

/// The opaque PubSub port instance.
struct fbp_pubsubp_s;

/// The port directional mode.
enum fbp_pubsubp_mode_e {
    /// Communicate downstream (server)
    FBP_PUBSUBP_MODE_DOWNSTREAM,
    /// Communicate upstream (client)
    FBP_PUBSUBP_MODE_UPSTREAM,
};

/**
 * @brief Port message type for port_data[3:0].
 *
 * port_data[7] is 1=retain for message types that need it.
 */
enum fbp_pubsubp_msg_e {
    /**
     * @brief Connection negotiation message for reliable state recovery.
     *
     * Format is fbp_pubsubp_msg_negotiate_s.
     *
     * This message allows each side to negotiate who supplies the retained
     * state.  When the connection is established, the downlink server sends
     * the request to the client with it's connection count.  The client
     * determines the source using this message, and replies to the server
     * responds by populating its connection_count and the resolution.
     *
     * If the client detects that server_connection_count == 1 or
     * client_connection_count > server_connection_count, then it resolves
     * to source=client.  The client then sends MSG_TOPIC_LIST without
     * RETAIN. The client then subscribes to the local PubSub instance
     * with RETAIN and forwards all retained values to server.  Once all
     * retained values have been sent, it sends MSG_CONNECTED.
     *
     * If the client detects that server_connection_count > client_connection_count,
     * or server_connection_count != 1 and force upstream state, then it
     * resolves to source=server.  The client then subscribes to the
     * local PubSub instance without RETAIN.  The client then sends MSG_TOPIC_LIST
     * with RETAIN, and the server forwards all matching retained values
     * to the client.  Once all retained values have been sent, it sends
     * MSG_CONNECTED.
     *
     * When connection is lost, issue fbp_pubsub_unsubscribe_from_all().
     */
    FBP_PUBSUBP_MSG_NEGOTIATE = 0,

    /**
     * @brief Update the list of subscribed topics.
     *
     * port_data[7] 0=no retained, 1=retained
     *
     * This message is sent from the client to the server to update
     * the subscribed topics, normally in response to a new connection
     * or connection re-establishment.  The subscription is always LINK.
     *
     * The payload is the unit-separator (0x1f) separated list of topics
     * to subscribe, which is compatible with _/topic/list.
     */
    FBP_PUBSUBP_MSG_TOPIC_LIST = 1,

    /**
     * @brief Add a topic subscription.
     *
     * port_data[7] 0=no retained, 1=retained
     *
     * payload is the null-terminated topic string.
     *
     * This message is sent from the client to the server to update
     * the subscribed topics, normally in response to _/topic/add.
     * The subscription is always LINK without RETAIN.
     */
    FBP_PUBSUBP_MSG_TOPIC_ADD = 2,

    /**
     * @brief Remove a topic subscription.
     *
     * payload is the null-terminated topic string.
     *
     * This message is sent from the client to the server to update
     * the subscribed topics, normally in response to _/topic/remove.
     */
    FBP_PUBSUBP_MSG_TOPIC_REMOVE = 3,

    /**
     * @brief Publish a topic.
     *
     * port_data[7] 0=no retained, 1=retained
     *
     * msg[0] is the fbp_union_e type
     * msg[1] reserved, write 0
     * msg[2] is the topic length.
     * msg[3:k] topic including null-termination
     * msg[k+3] is the payload length
     * msg[k+4:] The payload.  Strings are null-terminated.
     */
    FBP_PUBSUBP_MSG_PUBLISH = 4,

    /**
     * @brief Signal that the connection is fully established.
     *
     * port_data: ignored
     *
     * msg[0]: status
     * msg[1]: 0=req, 1=rsp
     */
    FBP_PUBSUBP_MSG_CONNECTED = 5,
};

#define FBP_PUBSUBP_PORT_DATA_MSG_MASK (0x0f)
#define FBP_PUBSUBP_PORT_DATA_RETAIN_BIT (0x80)

/**
 * @brief The FBP_PUBSUBP_MSG_NEGOTIATE payload.
 */
struct fbp_pubsubp_msg_negotiate_s {
    /// The major8.minor8.patch16 version.
    uint32_t version;
    uint8_t status;       // req:0, rsp:0=success or error code
    uint8_t resolution;   // 0=server provides state, 1=client provides state
    uint8_t msg_type;     // 0=request from server, 1=response from client.
    uint8_t rsv1_u8;
    uint64_t client_connection_count;
    uint64_t server_connection_count;
};

/**
 * @brief Create and initialize a new PubSub port instance.
 *
 * @param pubsub The pubsub instance.
 * @parma evm The event manager instance.
 * @param mode The port mode.
 * @return The new PubSub port instance.
 *
 * To ensure appropriate forwarding of subscribed topics,
 * this module will only on subscribe to the pubsub instance once
 * it establishes the connection.
 */
FBP_API struct fbp_pubsubp_s * fbp_pubsubp_initialize(struct fbp_pubsub_s * pubsub,
                                                      struct fbp_evm_api_s * evm,
                                                      enum fbp_pubsubp_mode_e mode);

/**
 * @brief Finalize the instance and free resources.
 *
 * @param self The PubSub port instance.
 */
FBP_API void fbp_pubsubp_finalize(struct fbp_pubsubp_s * self);

/**
 * @brief Register the transport instance.
 *
 * @param self The PubSub port instance.
 * @param port_id The port id.
 * @param transport The transport instance.
 * @return 0 or error.
 *
 * This instance uses the following transport functions:
 * - fbp_transport_port_register
 * - fbp_transport_send
 */
FBP_API int32_t fbp_pubsubp_transport_register(struct fbp_pubsubp_s * self,
                                               uint8_t port_id,
                                               struct fbp_transport_s * transport);

/**
 * @brief The function called on events.  [unit test]
 *
 * @param self The pubsub port instance.
 * @param event The signaled event.
 *
 * Can safely cast to fbp_transport_event_fn.
 */
FBP_API void fbp_pubsubp_on_event(struct fbp_pubsubp_s *self, enum fbp_dl_event_e event);

/**
 * @brief The function called upon message receipt.  [unit test]
 *
 * @param self The pubsub port instance.
 * @param port_id The port id for this port.
 * @param seq The frame reassembly information.
 * @param port_data The arbitrary 8-bit port data.  Each port is
 *      free to assign meaning to this value.
 * @param msg The buffer containing the message.
 *      This buffer is only valid for the duration of the callback.
 * @param msg_size The size of msg_buffer in bytes.
 *
 * Can safely cast to fbp_transport_recv_fn.
 */
FBP_API void fbp_pubsubp_on_recv(struct fbp_pubsubp_s *self,
                                 uint8_t port_id,
                                 enum fbp_transport_seq_e seq,
                                 uint8_t port_data,
                                 uint8_t *msg, uint32_t msg_size);

/**
 * @brief Function called on topic updates.
 *
 * @param self The pubsub port instance.
 * @param topic The topic for this update.
 * @param value The value for this update.
 * @return 0 or error code.
 *
 * Can safely cast to fbp_pubsub_subscribe_fn.
 */
FBP_API uint8_t fbp_pubsubp_on_update(struct fbp_pubsubp_s *self,
                                      const char * topic, const struct fbp_union_s * value);


/**
 * @brief Get the feedback topic used by this instance.
 *
 * @param self The pubsub port instance.
 * @return The feedback topic string.
 * @note Normally only needed for unit testing.
 */
FBP_API const char * fbp_pubsubp_feedback_topic(struct fbp_pubsubp_s *self);

FBP_CPP_GUARD_END

/** @} */

#endif  /* FBP_COMM_PUBSUB_PORT_H_ */
