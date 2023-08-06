
/**************************************************************************
 *                                                                        *
 *  Regina - A Normal Surface Theory Calculator                           *
 *  Computational Engine                                                  *
 *                                                                        *
 *  Copyright (c) 1999-2021, Ben Burton                                   *
 *  For further details contact Ben Burton (bab@debian.org).              *
 *                                                                        *
 *  This program is free software; you can redistribute it and/or         *
 *  modify it under the terms of the GNU General Public License as        *
 *  published by the Free Software Foundation; either version 2 of the    *
 *  License, or (at your option) any later version.                       *
 *                                                                        *
 *  As an exception, when this program is distributed through (i) the     *
 *  App Store by Apple Inc.; (ii) the Mac App Store by Apple Inc.; or     *
 *  (iii) Google Play by Google Inc., then that store may impose any      *
 *  digital rights management, device limits and/or redistribution        *
 *  restrictions that are required by its terms of service.               *
 *                                                                        *
 *  This program is distributed in the hope that it will be useful, but   *
 *  WITHOUT ANY WARRANTY; without even the implied warranty of            *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU     *
 *  General Public License for more details.                              *
 *                                                                        *
 *  You should have received a copy of the GNU General Public             *
 *  License along with this program; if not, write to the Free            *
 *  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,       *
 *  MA 02110-1301, USA.                                                   *
 *                                                                        *
 **************************************************************************/

/*! \file triangulation/detail/isosig-impl.h
 *  \brief Contains some of the implementation details for the generic
 *  Triangulation class template.
 *
 *  This file is \e not included from triangulation.h, but the routines
 *  it contains are explicitly instantiated in Regina's calculation engine.
 *  Therefore end users should never need to include this header.
 */

#ifndef __ISOSIG_IMPL_H_DETAIL
#ifndef __DOXYGEN
#define __ISOSIG_IMPL_H_DETAIL
#endif

#include <algorithm>
#include "triangulation/generic/triangulation.h"
#include "utilities/sigutils.h"

namespace regina {

template <int dim>
typename IsoSigPrintable<dim>::SigType IsoSigPrintable<dim>::encode(
        size_t nCompSimp, size_t nFacetActions, const char* facetAction,
        size_t nJoins, const size_t* joinDest,
        const typename Perm<dim + 1>::Index *joinGluing) {
    // We need to encode:
    // - the number of simplices in this component;
    // - facetAction[...];
    // - joinDest[...];
    // - joinGluing[...].
    std::string ans;

    // Keep it simple for small triangulations (1 character per integer).
    // For large triangulations, start with a special marker followed by
    // the number of chars per integer.
    unsigned nChars;
    if (nCompSimp < 63)
        nChars = 1;
    else {
        nChars = 0;
        size_t tmp = nCompSimp;
        while (tmp > 0) {
            tmp >>= 6;
            ++nChars;
        }

        ans = encodeSingle(63);
        ans += encodeSingle(nChars);
    }

    // Off we go.
    size_t i;
    encodeInt(ans, nCompSimp, nChars);
    for (i = 0; i < nFacetActions; i += 3)
        ans += encodeTrits(facetAction + i,
            (nFacetActions >= i + 3 ? 3 : nFacetActions - i));
    for (i = 0; i < nJoins; ++i)
        encodeInt(ans, joinDest[i], nChars);
    for (i = 0; i < nJoins; ++i)
        encodeInt(ans, joinGluing[i], charsPerPerm);

    return ans;
}

namespace detail {

template <int dim>
template <class Encoding>
typename Encoding::SigType TriangulationBase<dim>::isoSigFrom(
        size_t simp, const Perm<dim+1>& vertices,
        Isomorphism<dim>* relabelling) const {
    // Only process the component that simp belongs to.

    // ---------------------------------------------------------------------
    // Data for reconstructing a triangulation from an isomorphism signature
    // ---------------------------------------------------------------------

    // The number of simplices.
    size_t nSimp = size();

    // What happens to each new facet that we encounter?
    // Options are:
    //   0 -> boundary
    //   1 -> joined to a simplex not yet seen [gluing perm = identity]
    //   2 -> joined to a simplex already seen
    // These actions are stored in lexicographical order by (simplex, facet),
    // but only once for each facet (so we "skip" gluings that we've
    // already seen from the other direction).
    size_t nFacets = ((dim + 1) * size() + countBoundaryFacets()) / 2;
    char* facetAction = new char[nFacets];

    // What are the destination simplices and gluing permutations for
    // each facet under case #2 above?
    // For gluing permutations, we store the index of the permutation in
    // Perm<dim+1>::orderedSn.
    size_t* joinDest = new size_t[nFacets];
    typedef typename Perm<dim+1>::Index PermIndex;
    PermIndex* joinGluing = new PermIndex[nFacets];

    // ---------------------------------------------------------------------
    // Data for finding the unique canonical isomorphism from this
    // connected component that maps (simplex, vertices) -> (0, 0..dim)
    // ---------------------------------------------------------------------

    // The image for each simplex and its vertices:
    ptrdiff_t* image = new ptrdiff_t[nSimp];
    Perm<dim+1>* vertexMap = new Perm<dim+1>[nSimp];

    // The preimage for each simplex:
    ptrdiff_t* preImage = new ptrdiff_t[nSimp];

    // ---------------------------------------------------------------------
    // Looping variables
    // ---------------------------------------------------------------------
    size_t facetPos, joinPos, nextUnusedSimp;
    size_t simpImg, simpSrc, dest;
    unsigned facetImg, facetSrc;
    const Simplex<dim>* s;

    // ---------------------------------------------------------------------
    // The code!
    // ---------------------------------------------------------------------

    std::fill(image, image + nSimp, -1);
    std::fill(preImage, preImage + nSimp, -1);

    image[simp] = 0;
    vertexMap[simp] = vertices.inverse();
    preImage[0] = simp;

    facetPos = 0;
    joinPos = 0;
    nextUnusedSimp = 1;

    // To obtain a canonical isomorphism, we must run through the simplices
    // and their facets in image order, not preimage order.
    //
    // This main loop is guaranteed to exit when (and only when) we have
    // exhausted a single connected component of the triangulation.
    for (simpImg = 0; simpImg < nSimp && preImage[simpImg] >= 0; ++simpImg) {
        simpSrc = preImage[simpImg];
        s = simplex(simpSrc);

        for (facetImg = 0; facetImg <= dim; ++facetImg) {
            facetSrc = vertexMap[simpSrc].preImageOf(facetImg);

            // INVARIANTS (held while we stay within a single component):
            // - nextUnusedSimp > simpImg
            // - image[simpSrc], preImage[image[simpSrc]] and vertexMap[simpSrc]
            //   are already filled in.

            // Work out what happens to our source facet.
            if (! s->adjacentSimplex(facetSrc)) {
                // A boundary facet.
                facetAction[facetPos++] = 0;
                continue;
            }

            // We have a real gluing.  Is it a gluing we've already seen
            // from the other side?
            dest = s->adjacentSimplex(facetSrc)->index();

            if (image[dest] >= 0)
                if (image[dest] < image[simpSrc] ||
                        (dest == simpSrc &&
                         vertexMap[simpSrc][s->adjacentFacet(facetSrc)]
                         < vertexMap[simpSrc][facetSrc])) {
                    // Yes.  Just skip this gluing entirely.
                    continue;
                }

            // Is it a completely new simplex?
            if (image[dest] < 0) {
                // Yes.  The new simplex takes the next available
                // index, and the canonical gluing becomes the identity.
                image[dest] = nextUnusedSimp++;
                preImage[image[dest]] = dest;
                vertexMap[dest] = vertexMap[simpSrc] *
                    s->adjacentGluing(facetSrc).inverse();

                facetAction[facetPos++] = 1;
                continue;
            }

            // It's a simplex we've seen before.  Record the gluing.
            joinDest[joinPos] = image[dest];
            joinGluing[joinPos] = (vertexMap[dest] *
                s->adjacentGluing(facetSrc) * vertexMap[simpSrc].inverse()).
                orderedSnIndex();
            ++joinPos;

            facetAction[facetPos++] = 2;
        }
    }

    // We have all we need.  Pack it all together into a string.
    typename Encoding::SigType ans = Encoding::encode(simpImg,
        facetPos, facetAction, joinPos, joinDest, joinGluing);

    // Record the canonical isomorphism if required.
    if (relabelling)
        for (size_t i = 0; i < simpImg; ++i) {
            relabelling->simpImage(i) = image[i];
            relabelling->facetPerm(i) = vertexMap[i];
        }

    // Done!
    delete[] image;
    delete[] vertexMap;
    delete[] preImage;
    delete[] facetAction;
    delete[] joinDest;
    delete[] joinGluing;

    return ans;
}

template <int dim>
template <class Encoding>
typename Encoding::SigType TriangulationBase<dim>::isoSig(
        Isomorphism<dim>** relabelling) const {
    // Make sure the user is not trying to do something illegal.
    if (relabelling && countComponents() != 1) {
        *relabelling = nullptr; // Return 0 to the user...
        relabelling = nullptr;  // ... and forget they asked for an isomorphism.
    }

    Isomorphism<dim>* currRelabelling = nullptr;
    if (relabelling) {
        *relabelling = new Isomorphism<dim>(size());
        currRelabelling = new Isomorphism<dim>(size());
    }

    if (isEmpty())
        return Encoding::emptySig();

    // The triangulation is non-empty.  Get a signature string for each
    // connected component.
    ComponentIterator it;
    size_t i;
    size_t simp;
    typename Perm<dim+1>::Index perm;
    typename Encoding::SigType curr;

    typename Encoding::SigType* comp =
        new typename Encoding::SigType[countComponents()];
    for (it = components().begin(), i = 0;
            it != components().end(); ++it, ++i) {
        for (simp = 0; simp < (*it)->size(); ++simp)
            for (perm = 0; perm < Perm<dim+1>::nPerms; ++perm) {
                curr = isoSigFrom<Encoding>((*it)->simplex(simp)->index(),
                    Perm<dim+1>::orderedSn[perm], currRelabelling);
                if ((simp == 0 && perm == 0) || (curr < comp[i])) {
                    comp[i].swap(curr);
                    if (relabelling)
                        std::swap(*relabelling, currRelabelling);
                }
            }
    }

    // Pack the components together.
    std::sort(comp, comp + countComponents());

    typename Encoding::SigType ans;
    for (i = 0; i < countComponents(); ++i)
        ans += comp[i];

    delete[] comp;
    delete currRelabelling;
    return ans;
}

template <int dim>
Triangulation<dim>* TriangulationBase<dim>::fromIsoSig(
        const std::string& sig) {
    std::unique_ptr<Triangulation<dim>> ans(new Triangulation<dim>());

    typename Triangulation<dim>::ChangeEventSpan span(ans.get());

    const char* c = sig.c_str();

    // Skip any leading whitespace.
    while (*c && ::isspace(*c))
        ++c;

    // Find the end of the string.
    const char* end = c;
    while (*end && ! ::isspace(*end))
        ++end;

    // Initial check for invalid characters.
    const char* d;
    for (d = c; d != end; ++d)
        if (! Base64SigEncoding::isValid(*d))
            return 0;
    for (d = end; *d; ++d)
        if (! ::isspace(*d))
            return 0;

    unsigned j;
    size_t pos, nSimp, nChars;
    while (c != end) {
        // Read one component at a time.
        nSimp = Base64SigEncoding::decodeSingle(*c++);
        if (nSimp < 63)
            nChars = 1;
        else {
            if (c == end)
                return 0;
            nChars = Base64SigEncoding::decodeSingle(*c++);
            if (c + nChars > end)
                return 0;
            nSimp = Base64SigEncoding::decodeInt<unsigned>(c, nChars);
            c += nChars;
        }

        if (nSimp == 0) {
            // Empty component.
            continue;
        }

        // Non-empty component; keep going.
        char* facetAction = new char[(dim+1) * nSimp + 2];
        size_t nFacets = 0;
        size_t facetPos = 0;
        size_t nJoins = 0;

        for ( ; nFacets < (dim+1) * nSimp; facetPos += 3) {
            if (c == end) {
                delete[] facetAction;
                return 0;
            }
            Base64SigEncoding::decodeTrits(*c++, facetAction + facetPos);
            for (j = 0; j < 3; ++j) {
                // If we're already finished, make sure the leftover trits
                // are zero.
                if (nFacets == (dim+1) * nSimp) {
                    if (facetAction[facetPos + j] != 0) {
                        delete[] facetAction;
                        return 0;
                    }
                    continue;
                }

                if (facetAction[facetPos + j] == 0)
                    ++nFacets;
                else if (facetAction[facetPos + j] == 1)
                    nFacets += 2;
                else if (facetAction[facetPos + j] == 2) {
                    nFacets += 2;
                    ++nJoins;
                } else {
                    delete[] facetAction;
                    return 0;
                }
                if (nFacets > (dim+1) * nSimp) {
                    delete[] facetAction;
                    return 0;
                }
            }
        }

        size_t* joinDest = new size_t[nJoins + 1];
        for (pos = 0; pos < nJoins; ++pos) {
            if (c + nChars > end) {
                delete[] facetAction;
                delete[] joinDest;
                return 0;
            }

            joinDest[pos] = Base64SigEncoding::decodeInt<unsigned>(c, nChars);
            c += nChars;
        }

        typename Perm<dim+1>::Index* joinGluing =
            new typename Perm<dim+1>::Index[nJoins + 1];
        for (pos = 0; pos < nJoins; ++pos) {
            if (c + IsoSigPrintable<dim>::charsPerPerm > end) {
                delete[] facetAction;
                delete[] joinDest;
                delete[] joinGluing;
                return 0;
            }

            joinGluing[pos] =
                Base64SigEncoding::decodeInt<typename Perm<dim+1>::Index>(c,
                    IsoSigPrintable<dim>::charsPerPerm);
            c += IsoSigPrintable<dim>::charsPerPerm;

            if (joinGluing[pos] >= Perm<dim+1>::nPerms ||
                    joinGluing[pos] < 0) {
                delete[] facetAction;
                delete[] joinDest;
                delete[] joinGluing;
                return 0;
            }
        }

        // End of component!
        Simplex<dim>** simp = new Simplex<dim>*[nSimp];
        for (pos = 0; pos < nSimp; ++pos)
            simp[pos] = ans->newSimplex();

        facetPos = 0;
        size_t nextUnused = 1;
        size_t joinPos = 0;
        Perm<dim+1> gluing;
        for (pos = 0; pos < nSimp; ++pos)
            for (j = 0; j <= dim; ++j) {
                // Already glued from the other side:
                if (simp[pos]->adjacentSimplex(j))
                    continue;

                if (facetAction[facetPos] == 0) {
                    // Boundary facet.
                } else if (facetAction[facetPos] == 1) {
                    // Join to new simplex.
                    if (nextUnused >= nSimp) {
                        delete[] facetAction;
                        delete[] joinDest;
                        delete[] joinGluing;
                        delete[] simp;
                        return 0;
                    }
                    simp[pos]->join(j, simp[nextUnused++], Perm<dim+1>());
                } else {
                    // Join to existing simplex.
                    gluing = Perm<dim+1>::orderedSn[joinGluing[joinPos]];
                    if (joinDest[joinPos] >= nextUnused ||
                            simp[joinDest[joinPos]]->adjacentSimplex(
                            gluing[j])) {
                        delete[] facetAction;
                        delete[] joinDest;
                        delete[] joinGluing;
                        delete[] simp;
                        return 0;
                    }
                    simp[pos]->join(j, simp[joinDest[joinPos]], gluing);
                    ++joinPos;
                }

                ++facetPos;
            }

        delete[] facetAction;
        delete[] joinDest;
        delete[] joinGluing;
        delete[] simp;
    }

    return ans.release();
}

template <int dim>
size_t TriangulationBase<dim>::isoSigComponentSize(const std::string& sig) {
    const char* c = sig.c_str();

    // Examine the first character.
    // Note that isValid also ensures that *c is non-null (i.e., it
    // detects premature end of string).
    if (! Base64SigEncoding::isValid(*c))
        return 0;
    size_t nSimp = Base64SigEncoding::decodeSingle(*c);
    if (nSimp < 63)
        return nSimp;

    // The number of simplices is so large that it requires several
    // characters to store.
    ++c;
    if (! *c)
        return 0;
    size_t nChars = Base64SigEncoding::decodeSingle(*c++);

    for (const char* d = c; d < c + nChars; ++d)
        if (! Base64SigEncoding::isValid(*d))
            return 0;
    return Base64SigEncoding::decodeInt<unsigned>(c, nChars);
}

} } // namespace regina::detail

#endif
