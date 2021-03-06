#pragma once

#include <util/logging.h>

#include <aws/core/auth/AWSCredentialsProvider.h>
#include <aws/core/Aws.h>

namespace awswrapper {

    std::shared_ptr<Aws::Auth::AWSCredentialsProvider> getCredentialsProvider();

    Aws::Client::ClientConfiguration getClientConf(long timeout=3000);

    void initSDK();
    void cleanUpSDK();

    template<typename T>
    void handleError(const Aws::Client::AWSError<T> err) {
        const std::shared_ptr<spdlog::logger> &logger = util::getLogger();
        logger->error("AWS error: {} {}", err.GetExceptionName().c_str(), err.GetMessage().c_str());

        throw std::runtime_error("AWS error");
    }
}