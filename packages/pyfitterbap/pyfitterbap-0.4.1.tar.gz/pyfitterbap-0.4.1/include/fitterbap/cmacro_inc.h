/*
 * Copyright 2014-2021 Jetperch LLC
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
 * @brief Commonly used C macros for FBP.
 */

#ifndef FBP_CMACRO_INC_H__
#define FBP_CMACRO_INC_H__

/**
 * @ingroup fbp_core
 * @defgroup fbp_cmacro_inc C Macros
 *
 * @brief Commonly used C macros for FBP.
 *
 * @{
 */

/**
 * @def FBP_CPP_GUARD_START
 * @brief Make a C header file safe for a C++ compiler.
 *
 * This guard should be placed at near the top of the header file after
 * the \#if and imports.
 */

/**
 * @def FBP_CPP_GUARD_END
 * @brief Make a C header file safe for a C++ compiler.
 *
 * This guard should be placed at the bottom of the header file just before
 * the \#endif.
 */

#if defined(__cplusplus) && !defined(__CDT_PARSER__)
#define FBP_CPP_GUARD_START extern "C" {
#define FBP_CPP_GUARD_END };
#else
#define FBP_CPP_GUARD_START
#define FBP_CPP_GUARD_END
#endif

/**
 * @brief All functions that are available from the library are marked with
 *      FBP_API.  This platform-specific definition allows DLLs to ber
 *      created properly on Windows.
 */
#if defined(FBP_EXPORT)
#define FBP_API __declspec(dllexport)
#elif defined(FBP_IMPORT)
#define FBP_API __declspec(dllimport)
#else
#define FBP_API
#endif

/**
 * @brief Declare a packed structure.
 */
#define FBP_STRUCT_PACKED __attribute__((packed))

#ifdef __GNUC__
#define FBP_USED __attribute__((used))
#define FBP_FORMAT __attribute__((format))
#else
#define FBP_USED
#endif

/** @} */

#endif /* FBP_CMACRO_INC_H__ */
