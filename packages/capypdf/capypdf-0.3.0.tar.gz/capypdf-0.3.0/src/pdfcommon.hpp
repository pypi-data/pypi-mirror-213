/*
 * Copyright 2022-2023 Jussi Pakkanen
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

#pragma once

#include <capypdf.h>
#include <errorhandling.hpp>

#include <optional>
#include <vector>
#include <array>
#include <functional>

#include <cstdint>

// This macro must not be used from within a namespace.
#define DEF_BASIC_OPERATORS(TNAME)                                                                 \
    inline bool operator==(const TNAME &object_number_1, const TNAME &object_number_2) {           \
        return object_number_1.id == object_number_2.id;                                           \
    }                                                                                              \
                                                                                                   \
    inline std::strong_ordering operator<=>(const TNAME &object_number_1,                          \
                                            const TNAME &object_number_2) {                        \
        return object_number_1.id <=> object_number_2.id;                                          \
    }                                                                                              \
                                                                                                   \
    template<> struct std::hash<TNAME> {                                                           \
        std::size_t operator()(const TNAME &tobj) const noexcept {                                 \
            return std::hash<int32_t>{}(tobj.id);                                                  \
        }                                                                                          \
    }

DEF_BASIC_OPERATORS(CapyPdF_ImageId);

DEF_BASIC_OPERATORS(CapyPdF_FontId);

DEF_BASIC_OPERATORS(CapyPdF_IccColorSpaceId);

DEF_BASIC_OPERATORS(CapyPdF_FormXObjectId);

DEF_BASIC_OPERATORS(CapyPdF_FormWidgetId);

DEF_BASIC_OPERATORS(CapyPdF_AnnotationId);

DEF_BASIC_OPERATORS(CapyPdF_StructureItemId);

namespace capypdf {

struct PdfBox {
    double x;
    double y;
    double w;
    double h;

    static PdfBox a4() { return PdfBox{0, 0, 595.28, 841.89}; }
};

struct PdfRectangle {
    double x1;
    double y1;
    double x2;
    double y2;
};

class LimitDouble {
public:
    LimitDouble() : value(minval) {}

    // No "explicit" because we want the following to work for convenience:
    // DeviceRGBColor{0.0, 0.3, 1.0}
    LimitDouble(double new_val) : value(new_val) { clamp(); }

    double v() const { return value; }

    LimitDouble &operator=(double d) {
        value = d;
        clamp();
        return *this;
    }

private:
    constexpr static double maxval = 1.0;
    constexpr static double minval = 0.0;

    void clamp() {
        if(value < minval) {
            value = minval;
        }
        if(value > maxval) {
            value = maxval;
        }
    }

    double value;
};

// Every resource type has its own id type to avoid
// accidentally mixing them up.

struct SeparationId {
    int32_t id;
};

struct GstateId {
    int32_t id;
};

struct FunctionId {
    int32_t id;
};

struct ShadingId {
    int32_t id;
};

struct PatternId {
    int32_t id;
};

struct LabId {
    int32_t id;
};

struct PageId {
    int32_t id;
};

struct OutlineId {
    int32_t id;
};

struct GraphicsState {
    std::optional<CapyPdF_Rendering_Intent> intent;
    std::optional<CAPYPDF_Blend_Mode> blend_mode;
    std::optional<bool> OP;
    std::optional<bool> op;
    std::optional<int32_t> OPM;
};

struct DeviceRGBColor {
    LimitDouble r;
    LimitDouble g;
    LimitDouble b;
};

struct DeviceGrayColor {
    LimitDouble v;
};

struct DeviceCMYKColor {
    LimitDouble c;
    LimitDouble m;
    LimitDouble y;
    LimitDouble k;
};

struct LabColor {
    double l;
    double a;
    double b;
};

struct LabColorSpace {
    double xw, yw, zw;
    double amin, amax, bmin, bmax;

    static LabColorSpace cielab_1976_D65() {
        LabColorSpace cl;
        cl.xw = 0.9505;
        cl.yw = 1.0;
        cl.zw = 1.089;

        cl.amin = -128;
        cl.amax = 127;
        cl.bmin = -128;
        cl.bmax = 127;
        return cl;
    }
};

struct FunctionType2 {
    std::vector<double> domain;
    std::vector<double> C0;
    std::vector<double> C1;
    double n;
};

// Linear
struct ShadingType2 {
    CapyPdF_Colorspace colorspace;
    double x0, y0, x1, y1;
    FunctionId function;
    bool extend0, extend1;
};

// Radial
struct ShadingType3 {
    CapyPdF_Colorspace colorspace;
    double x0, y0, r0, x1, y1, r1;
    FunctionId function;
    bool extend0, extend1;
};

struct TextStateParameters {
    std::optional<double> char_spacing;
    std::optional<double> word_spacing;
    std::optional<double> horizontal_scaling;
    std::optional<double> leading;
    std::optional<CapyPdF_Text_Mode> render_mode;
    std::optional<double> rise;
    // Knockout can only be set with gs.
};

struct FontSubset {
    CapyPdF_FontId fid;
    int32_t subset_id;

    bool operator==(const FontSubset &other) const {
        return fid.id == other.fid.id && subset_id == other.subset_id;
    }

    bool operator!=(const FontSubset &other) const { return !(*this == other); }
};

extern const std::array<const char *, 4> rendering_intent_names;

struct PageTransition {
    std::optional<CAPYPDF_Transition_Type> type;
    std::optional<double> duration;
    std::optional<bool> Dm;    // true is horizontal
    std::optional<bool> M;     // true is inward
    std::optional<int32_t> Di; // FIXME, turn into an enum and add none
    std::optional<double> SS;
    std::optional<bool> B;
};

} // namespace capypdf
