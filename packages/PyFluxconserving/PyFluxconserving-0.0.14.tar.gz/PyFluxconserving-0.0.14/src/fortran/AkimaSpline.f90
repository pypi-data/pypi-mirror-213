! ###########################################################################
!     RESUME : Akima Spline interpolation. The Akima spline is a C1         !
!     differentiable function (that is, has a continuous first derivative)  !
!     but, in general, will have a discontinuous second derivative at the   !
!     knot points.                                                          !
!                                                                           !
!     [1]: Akima, H. (1970). A New Method of Interpolation and Smooth Curve !
!          Fitting Based on Local Procedures. Journal of the ACM, 17(4),    !
!          589-602. Association for Computing                               !
!          Machinery. doi:10.1145/321607.321609                             !
!                                                                           !
!     PYTHON : Python compatibility using f2py revised. Better usage        !
!              with numpy.                                                  !
!                                                                           !
!     Written: Jean Michel Gomes                                            !
!     Checked: Wed May  2 10:00:52 WEST 2012                                !
!              Fri Dec 28 13:53:36 WET  2012                                !
!              Sun Mar 10 10:05:03 WET  2013                                !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! ###########################################################################
!     RESUME : Absolute value function with small quadratic parabola-like   !
!              in the valley so that it is C1 continuous. C1 continuous     !
!              - Continuous first derivative.                               !
!                                                                           !
!     Input           arguments = 2                                         !
!     Output          arguments = 1                                         !
!     Optional        arguments = 0                                         !
!     Total number of arguments = 3                                         !
!                                                                           !
!     INPUT  : 01) x       -> Input value                                   !
!              02) delta_x -> Valley window point to be quadratic           !
!                                                                           !
!     OUTPUT : 01) y       -> Output value                                  !
!                                                                           !
!     PYTHON : Python compatibility using f2py revised. Better usage        !
!              with numpy.                                                  !
!                                                                           !
!     Written: Jean Michel Gomes                                            !
!     Checked: Tue May  1 16:09:13 WEST 2012                                !
!              Fri Dec 28 14:55:10 WET  2012                                !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SUBROUTINE ABS__smooth( x,y,delta_x )
    use ModDataType
    implicit none
    
    ! --- input data ---
    real     (kind=RP), intent(in) :: x, delta_x

    ! --- output data --
    real     (kind=RP), intent(out) :: y

    !f2py real     (kind=RP), intent(in) :: x
    !f2py real     (kind=RP), intent(out) :: y
    !f2py real     (kind=RP), intent(in) :: delta_x = 0.1
    
    if ( x >= delta_x ) then
       y = x
    else if ( x <= -delta_x ) then
       y = -x
    else
       y = x*x / (2.0_RP*delta_x) + delta_x / 2.0_RP
    end if 

END SUBROUTINE ABS__smooth
! ###########################################################################

! ###########################################################################
!     RESUME : Compute the Spline Coefficients for the Akima Spline         !
!              function.                                                    !
!                                                                           !
!     Input           arguments = 4                                         !
!     Output          arguments = 4                                         !
!     Optional        arguments = 0                                         !
!     Total number of arguments = 8                                         !
!                                                                           !
!     INPUT  : 01) xold_vec -> Original Abscissa                            !
!              02) yold_vec -> Original Ordinate                            !
!              03) nold_vec -> # of Points                                  !
!              04) delta__x -> Valley window point to be quadratic          !
!                                                                           !
!     OUTPUT : 01) p0       -> Spline Coefficient                           !
!              02) p1       -> Spline Coefficient                           !
!              03) p2       -> Spline Coefficient                           !
!              04) p3       -> Spline Coefficient                           !
!                                                                           !
!     PYTHON : Python compatibility using f2py revised. Better usage        !
!              with numpy.                                                  !
!                                                                           !
!     Written: Jean Michel Gomes                                            !
!     Checked: Wed May  2 10:00:52 WEST 2012                                !
!              Fri Dec 28 13:53:36 WET  2012                                !
!              Sun Mar 10 10:05:03 WET  2013                                !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SUBROUTINE Akima_Setup( xold_vec,yold_vec,nold_vec,p0,p1,p2,p3,delta__x )
    use ModDataType
    implicit none

    real     (kind=RP), parameter :: eps = 1.0e-30_RP

    ! --- input data ---
    integer  (kind=IB), intent(in) :: nold_vec
    real     (kind=RP), dimension(0:nold_vec-1), intent(in) :: xold_vec,    &
                                                               yold_vec     ! Original points
    real     (kind=RP), intent(in) :: delta__x

    ! --- output data --
    real     (kind=RP), dimension(0:nold_vec-2), intent(out) :: p0, p1, p2, &
                                                                p3          ! Spline Coefficients

    ! --- local variables 
    integer  (kind=IB) :: i!,j
    real     (kind=RP), dimension(-2:nold_vec) :: m
    real     (kind=RP), dimension(0:nold_vec-1) :: t
    real     (kind=RP) :: m1, m2, m3, m4, w1, w2
    real     (kind=RP) :: t1, t2, dx

    !f2py real     (kind=RP), intent(in) :: xold_vec,yold_vec
    !f2py                     intent(hide), depend(xold_vec) :: n=shape(xold_vec,0)
    !f2py                     intent(hide), depend(yold_vec) :: n=shape(yold_vec,0)

    !f2py real     (kind=RP), intent(out) :: p0,p1,p2,p3
    !f2py                     intent(hide), depend(p0) :: m=shape(p0,0)
    !f2py                     intent(hide), depend(p1) :: m=shape(p1,0)
    !f2py                     intent(hide), depend(p2) :: m=shape(p2,0)
    !f2py                     intent(hide), depend(p3) :: m=shape(p3,0)
    
    !f2py real     (kind=RP), intent(in) :: delta__x = 0.1

    ! --- Compute Slope Segments ---
    do i=0,nold_vec-2
       !if ( xold_vec(i+1) /= xold_vec(i) ) then
       m(i) = (yold_vec(i+1) - yold_vec(i)) / (xold_vec(i+1) - xold_vec(i))
       !else
       !   if ( i > 1 ) then
       !      m(i) = m(i-1)
       !   end if
       !   if ( i == 1 .and. i+2<nold_vec-1 ) then
       !      j = i+1
       !      do while ( j < nold_vec-1 .and. xold_vec(j) == xold_vec(i) )
       !         j=j+1
       !         m(i) = (yold_vec(j) - yold_vec(i)) / (xold_vec(j) - xold_vec(i))
       !      end do
       !   end if
       !end if
    end do

    ! --- Estimation for end points
    m(0       -1) = 2.0_RP * m(0       +0) - m(0       +1)
    m(0       -2) = 2.0_RP * m(0       -1) - m(0       +0)
    m(nold_vec-1) = 2.0_RP * m(nold_vec-2) - m(nold_vec-3)
    m(nold_vec+0) = 2.0_RP * m(nold_vec-1) - m(nold_vec-2)

    ! --- Slope at points
    do i=0,nold_vec-1
       m1 = m(i-2)
       m2 = m(i-1)
       m3 = m(i)
       m4 = m(i+1)

!       w1 = abs(m4 - m3)
!       w2 = abs(m2 - m1)

       call ABS__smooth( m4 - m3, w1, delta__x )
       call ABS__smooth( m2 - m1, w2, delta__x )

       if ( w1 < eps .and. w2 < eps ) then
          t(i) = 0.5_RP*(m2 + m3)                                           ! --- Avoid division by zero
       else
          t(i) = (w1*m2 + w2*m3) / (w1 + w2)
       end if
    end do

! --- Compute Polynomial Cofficients ----------------------------------------
    do i=0,nold_vec-2
       dx    = xold_vec(i+1) - xold_vec(i)
       t1    = t(i)
       t2    = t(i+1)
       p0(i) = yold_vec(i)
       p1(i) = t1
       p2(i) = (3.0_RP*m(i) - 2.0_RP*t1 - t2)/dx
       !p3(i) = (t1 + t2 - 2.0_RP*m(i))/dx**2
       p3(i) = (t1 + t2 - 2.0_RP*m(i))/(dx*dx)
    end do
! --- Compute Polynomial Cofficients ----------------------------------------
    
    return
END SUBROUTINE Akima_Setup
! ###########################################################################

! ###########################################################################
!     RESUME : Evaluate the Akima Spline and its derivatives.  The          !
!              Akima spline is a C1 differentiable unction (that is,        !
!              has a continuous first derivative) but, in general,          !
!              will have a discontinuous second derivative at the knot      !
!              points.                                                      !
!                                                                           !
!     Input           arguments = 16                                        !
!     Output          arguments = 4                                         !
!     Optional        arguments = 1                                         !
!     Total number of arguments = 21                                        !
!                                                                           !
!     INPUT  : 01) xx_value -> New interpolated x array with points         !
!              02) nxyvalue -> # of elements in xx_value and yy_value       !
!              03) xold_vec -> Old x vector (abcissas)                      !
!              04) nold_vec -> # of elements in xold_vec and yold_vec       !
!              05) p0       -> Spline Coefficient                           !
!              06) p1       -> Spline Coefficient                           !
!              07) p2       -> Spline Coefficient                           !
!              08) p3       -> Spline Coefficient                           !
!              09) dp0dxold -> Derivatives of coefficients                  !
!              10) dp1dxold -> Derivatives of coefficients                  !
!              11) dp2dxold -> Derivatives of coefficients                  !
!              12) dp3dxold -> Derivatives of coefficients                  !
!              13) dp0dyold -> Derivatives of coefficients                  !
!              14) dp1dyold -> Derivatives of coefficients                  !
!              15) dp2dyold -> Derivatives of coefficients                  !
!              16) dp3dyold -> Derivatives of coefficients                  !
!              17) Is_Deriv -> Is derivative on:1 or off:0                  !
!              18) Is_Index -> Search: Linear: [1] & Binary [0]             !
!                                                                           !
!     OUTPUT : 01) yy_value -> New interpolated yy_value array              !
!              02) dy____dx -> Derivative of yy_value w.r.t. xx_value       !
!              03) dy_dxold -> Derivative of yy_value w.r.t. yold_vec       !
!              04) dy_dyold -> Derivative of yy_value w.r.t. yold_vec       !
!                                                                           !
!     PYTHON : Python compatibility using f2py revised. Better usage        !
!              with numpy.                                                  !
!                                                                           !
!     Written: Jean Michel Gomes                                            !
!     Checked: Wed May  2 10:00:52 WEST 2012                                !
!              Fri Dec 28 13:53:36 WET  2012                                !
!              Sun Mar 10 10:05:03 WET  2013                                !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SUBROUTINE Akimainterp( xx_value,yy_value,nx_value,xold_vec,nold_vec,p0,p1, &
                        p2,p3   ,dp0dxold,dp1dxold,dp2dxold,dp3dxold,       &
                        dp0dyold,dp1dyold,dp2dyold,dp3dyold,dy____dx,       &
                        dy_dxold,dy_dyold,Is_Deriv,Is_Index )
    use ModDataType
    implicit none
    
    ! --- input data ---
    integer  (kind=IB), intent(in) :: nold_vec
    integer  (kind=IB), intent(in) :: nx_value
    integer  (kind=IB), optional :: Is_Deriv,Is_Index

    real     (kind=RP), dimension(0:nold_vec-1), intent(in) :: xold_vec     ! Original x (abscissa) points
    real     (kind=RP), dimension(0:nold_vec-2), intent(in) :: p0,p1,p2,p3  ! Spline Coefficients

    real     (kind=RP), dimension(0:nx_value-1), intent(in) :: xx_value     ! New x values to evaluate y
    real     (kind=RP), dimension(0:nold_vec-2,0:nold_vec-1), intent(in) :: &
                                                                  dp0dxold, &
                                                                  dp1dxold, &
                                                                  dp2dxold, &
                                                                  dp3dxold
    real     (kind=RP), dimension(0:nold_vec-2,0:nold_vec-1), intent(in) :: &
                                                                  dp0dyold, &
                                                                  dp1dyold, &
                                                                  dp2dyold, &
                                                                  dp3dyold
    
    ! --- output data --
    real     (kind=RP), dimension(0:nx_value-1), intent(out) :: yy_value         ! New interpolated y values
    real     (kind=RP), dimension(0:nx_value-1), intent(out) :: dy____dx         ! Derivative of yy_values with respect to xx_values (new values)
    real     (kind=RP), dimension(0:nx_value-1,0:nold_vec-1), intent(out) ::&
                                                                  dy_dxold, &
                                                                  dy_dyold       ! Derivatives of yy_value with respect to xold_vec and yold_vec

    ! --- local variables
    integer  (kind=IB) :: i, j, k
    integer  (kind=IB) :: ii, jj, Derivatives, indice
    real     (kind=RP) :: dx,dx2,dx3

    !f2py real     (kind=RP), intent(in) :: xold_vec,yold_vec
    !f2py                     intent(hide), depend(xold_vec) :: nold_vec=shape(xold_vec,0)
    !f2py                     intent(hide), depend(yold_vec) :: nold_vec=shape(yold_vec,0)

    !f2py real     (kind=RP), intent(in) :: xx_value
    !f2py                     intent(hide), depend(xx_value) :: nxyvalue=shape(xx_value,0)
    
    !f2py real     (kind=RP), intent(out) :: yy_value
    !f2py                     intent(hide), depend(yy_value) :: nxyvalue=shape(yy_value,0)

    !f2py real     (kind=RP), intent(in) :: p0,p1,p2,p3
    !f2py                     intent(hide), depend(p0) :: m=shape(p0,0)
    !f2py                     intent(hide), depend(p1) :: m=shape(p1,0)
    !f2py                     intent(hide), depend(p2) :: m=shape(p2,0)
    !f2py                     intent(hide), depend(p3) :: m=shape(p3,0)

    !f2py real     (kind=RP), intent(in) :: dp0dxold
    !f2py real     (kind=RP), intent(in) :: dp1dxold
    !f2py real     (kind=RP), intent(in) :: dp2dxold
    !f2py real     (kind=RP), intent(in) :: dp3dxold
    !f2py real     (kind=RP), intent(in) :: dp0dyold
    !f2py real     (kind=RP), intent(in) :: dp1dyold
    !f2py real     (kind=RP), intent(in) :: dp2dyold
    !f2py real     (kind=RP), intent(in) :: dp3dyold

    !f2py                     intent(hide), depend(dp0dxold) :: m=shape(dp0dxold,0), nold_vec=shape(dp0dxold,1)
    !f2py                     intent(hide), depend(dp1dxold) :: m=shape(dp1dxold,0), nold_vec=shape(dp1dxold,1)
    !f2py                     intent(hide), depend(dp2dxold) :: m=shape(dp2dxold,0), nold_vec=shape(dp2dxold,1)
    !f2py                     intent(hide), depend(dp3dxold) :: m=shape(dp3dxold,0), nold_vec=shape(dp3dxold,1)
    !f2py                     intent(hide), depend(dp0dyold) :: m=shape(dp0dyold,0), nold_vec=shape(dp0dyold,1)
    !f2py                     intent(hide), depend(dp1dyold) :: m=shape(dp1dyold,0), nold_vec=shape(dp1dyold,1)
    !f2py                     intent(hide), depend(dp2dyold) :: m=shape(dp2dyold,0), nold_vec=shape(dp2dyold,1)
    !f2py                     intent(hide), depend(dp3dyold) :: m=shape(dp3dyold,0), nold_vec=shape(dp3dyold,1)

    
    !f2py real     (kind=RP), intent(out) :: dy____dx
    !f2py                     intent(hide), depend(dy____dx) :: nx_value=shape(dp0dxold,0)
    
    !f2py real     (kind=RP), intent(out) :: dy_dxold
    !f2py real     (kind=RP), intent(out) :: dy_dyold
    !f2py                     intent(hide), depend(dy_dxold) :: nx_value=shape(dy_dxold,0), nold_vec=shape(dy_dxold,1)
    !f2py                     intent(hide), depend(dy_dyold) :: nx_value=shape(dy_dyold,0), nold_vec=shape(dy_dyold,1)
    
    !f2py integer  (kind=IB), optional :: Is_Deriv=0
    !f2py integer  (kind=IB), optional :: Is_Index=0

    
    if ( present(Is_Deriv) ) then
       Derivatives = Is_Deriv 
    else
       Derivatives = 0_IB
    end if

    if ( present(Is_Index) ) then
       indice = Is_Index
    else
       indice = 0_IB
    end if

    !if ( Derivatives == 0_IB ) then
    !   dy____dx = 0.0_RP
    !   dy_dxold = 0.0_RP
    !   dy_dyold = 0.0_RP
    !end if
    
! --- Interpolate at each new point x ---------------------------------------
    j = 0
    do i=0,nx_value-1

! --- Find indexes in arrays ------------------------------------------------

! --- Use initial or end segments if outside boundaries / extrapolate -------
       if ( xx_value(i) <= xold_vec(0) ) then
          j = 0
       end if

       if ( xx_value(i) >= xold_vec(nold_vec-1) ) then
          j = nold_vec-2
       end if

       if ( indice == 1_IB ) then
          ! Normal Search
          if ( xx_value(i) > xold_vec(0) .and. &
               xx_value(i) < xold_vec(nold_vec-1) ) then
             ! linear search for now
             do j = nold_vec-2,1,-1
                if ( xx_value(i) >= xold_vec(j) ) then
                   exit
                end if
             end do
          end if
       else
          ! Binary Search
          if ( xx_value(i) > xold_vec(0) .and.                              &
               xx_value(i) < xold_vec(nold_vec-1) ) then
             ii = 0
             jj = nold_vec
             do while (jj > ii+1)
                k = (ii+jj)/2
                if (xx_value(i) < xold_vec(k)) then
                   jj=k
                else
                   ii=k
                end if
             end do
             !       i = 1
             !       j = n+1
             !20     k = (i+j)/2
             !       if ( u  < xx_value(K) ) j = k
             !       if ( u >= xx_value(K) ) i = k
             !       if ( j  > i+1  ) go to 20
             j = ii
          end if
          !write (*,*) j
       end if

       ! --- Evaluate polynomials and derivatives ---
       dx      = xx_value(i) - xold_vec(j)
       dx2     = dx  * dx
       dx3     = dx2 * dx
       
       !yy_value(i) = p0(j) + p1(j)*dx + p2(j)*dx**2 + p3(j)*dx**3
       !dy____dx(i) = p1(j) + 2.0_RP*p2(j)*dx + 3.0_RP*p3(j)*dx**2
       
       yy_value(i) = p0(j) + p1(j)*dx + p2(j)*dx2 + p3(j)*dx3

       ! *** Compute derivatives
       if ( Derivatives == 1_IB ) then
          dy____dx(i) = p1(j) + 2.0_RP*p2(j)*dx + 3.0_RP*p3(j)*dx2
          do k=0,nold_vec-1

             !dy_dxold(i,k) = dp0dxold(j,k) + dp1dxold(j,k)*dx              &
             !              + dp2dxold(j,k)*dx**2&
             !              + dp3dxold(j,k)*dx**3
             dy_dxold(i,k) = dp0dxold(j,k) + dp1dxold(j,k)*dx               &
                           + dp2dxold(j,k)*dx2                              &
                           + dp3dxold(j,k)*dx3

             if ( k == j ) then
                dy_dxold(i,k) = dy_dxold(i,k) - dy____dx(i)
             end if

             !dy_dyold(i,k) = dp0dyold(j,k) + dp1dyold(j,k)*dx              &
             !              + dp2dyold(j,k)*dx**2&
             !              + dp3dyold(j,k)*dx**3

             dy_dyold(i,k) = dp0dyold(j,k) + dp1dyold(j,k)*dx               &
                           + dp2dyold(j,k)*dx2 + dp3dyold(j,k)*dx3
          end do
       end if

    end do
! --- Interpolate at each new point x ---------------------------------------

    return
END SUBROUTINE Akimainterp
! ###########################################################################

! ###########################################################################
!     RESUME : For a given array of values 'xx_value' for the               !
!              abscissa, then return the ordinate array values of           !
!              'yy_value' based on Akima Spline interpolation.              !
!                                                                           !
!     INPUT  : 01) xx_value  -> New interpolated x array with points        !
!              02) nxyvalue  -> # of elements in xx_value and yy_value      !
!              03) xold_vec  -> Old x vector (abcissas)                     !
!              04) yold_vec  -> Old y vector (ordenadas)                    !
!              05) nold_vec  -> # of elements in xold_vec and yold_vec      !
!              06) delta__x  -> Value used in the absolute value function   !
!                               with small quadratic parabola-like in the   !
!                               valley so that it is C1 continuous. C1      !
!                               continuous                                  !
!              07) verbosity -> Print & Check screen                        !
!                                                                           !
!     OUTPUT : 01) yy_value -> New interpolated y array with points         !
!              02) IsKeepOn -> Flag, if == 0 then there's a problem         !
!                                                                           !
!     PYTHON : Python compatibility using f2py revised. Better usage        !
!              with numpy.                                                  !
!                                                                           !
!     Written: Jean Michel Gomes                                            !
!     Checked: Wed May  2 10:00:52 WEST 2012                                !
!              Fri Dec 28 13:53:36 WET  2012                                !
!              Sun Mar 10 10:05:03 WET  2013                                !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SUBROUTINE AkimaSpline( xx_value,yy_value,nxyvalue,xold_vec,yold_vec,       &
                        nold_vec,delta__x,IsKeepOn,verbosity )

    use ModDataType
    implicit none

    integer  (kind=IB), intent(in) :: nold_vec, nxyvalue
    integer  (kind=IB), optional :: verbosity
    integer  (kind=IB) :: IsShowOn,Is_Deriv,Is_Index

    integer  (kind=IB), intent(out) :: IsKeepOn
    
    real     (kind=RP), dimension(0:nold_vec-1), intent(in)  :: xold_vec,   &
                                                                yold_vec
    real     (kind=RP), dimension(0:nxyvalue-1), intent(in)  :: xx_value
    real     (kind=RP), dimension(0:nxyvalue-1), intent(out) :: yy_value

    real     (kind=RP), dimension(0:nold_vec-2,0:nold_vec-1) :: zero_vec

    real     (kind=RP), dimension(0:nxyvalue-1) :: dy_dxnew                 ! Derivative of yy_value with respect to xx_value
    real     (kind=RP), dimension(0:nxyvalue-1,0:nold_vec-1) :: dy_dxold,   &
                                                                dy_dyold    ! Derivative of yold_vec with respect to xold_vec and yold_vec


    real     (kind=RP), dimension(0:nold_vec-2) :: p0, p1, p2, p3           ! Spline Coefficients
    real     (kind=RP), intent(in) :: delta__x

    !f2py real     (kind=RP), intent(in) :: xold_vec,yold_vec
    !f2py                     intent(hide), depend(xold_vec) :: nold_vec=shape(xold_vec,0)
    !f2py                     intent(hide), depend(yold_vec) :: nold_vec=shape(yold_vec,0)

    !f2py real     (kind=RP), intent(in) :: xx_value
    !f2py                     intent(hide), depend(xx_value) :: nxyvalue=shape(xx_value,0)
    
    !f2py real     (kind=RP), intent(out) :: yy_value
    !f2py                     intent(hide), depend(yy_value) :: nxyvalue=shape(yy_value,0)

    !f2py real     (kind=RP), intent(in) :: delta__x = 0.1
    !f2py integer  (kind=IB), optional :: verbosity=0

    interface
       subroutine Akimainterp( xx_value,yy_value,nx_value,xold_vec,nold_vec,&
                               p0,p1,p2,p3,dp0dxold,dp1dxold,dp2dxold,      &
                               dp3dxold,dp0dyold,dp1dyold,dp2dyold,dp3dyold,&
                               dy____dx,dy_dxold,dy_dyold,Is_Deriv,Is_Index )
         use ModDataType
         integer  (kind=IB), intent(in) :: nold_vec
         integer  (kind=IB), intent(in) :: nx_value
         integer  (kind=IB), optional :: Is_Deriv,Is_Index
         real     (kind=RP), dimension(0:nold_vec-1), intent(in) :: xold_vec          ! Original x (abscissa) points
         real     (kind=RP), dimension(0:nold_vec-2), intent(in) :: p0,p1,  &
                                                                    p2,p3             ! Spline Coefficients
         real     (kind=RP), dimension(0:nx_value-1), intent(in) :: xx_value          ! New x values to evaluate y
         real     (kind=RP), dimension(0:nold_vec-2,0:nold_vec-1),          &
                                                            intent(in) ::   &
                                                            dp0dxold,       &
                                                            dp1dxold,       &
                                                            dp2dxold,       &
                                                            dp3dxold
         real     (kind=RP), dimension(0:nold_vec-2,0:nold_vec-1),          &
                                                            intent(in) ::   &
                                                            dp0dyold,       &
                                                            dp1dyold,       &
                                                            dp2dyold,       &
                                                            dp3dyold
         real     (kind=RP), dimension(0:nx_value-1), intent(out) :: yy_value         ! New interpolated y values
         real     (kind=RP), dimension(0:nx_value-1), intent(out) :: dy____dx         ! Derivative of y with respect to x (new values)
         real     (kind=RP), dimension(0:nx_value-1,0:nold_vec-1),          &
                                                              intent(out) ::&
                                                            dy_dxold,       &
                                                            dy_dyold                  ! Derivatives of y with respect to xold and yold

       end subroutine Akimainterp
    end interface

    IsKeepOn = 1_IB
    
    if ( present(verbosity) ) then
        IsShowOn = verbosity
    else
        IsShowOn = 0_IB
    end if

    if ( IsShowOn == 1_IB ) then
       write (*,'(4x,a)') '[AkimaSpline]'
    end if

    !if ( count(xold_vec(1:nold_vec-1)-xold_vec(0:nold_vec-2) < 0) > 0 ) then
    !   if ( IsShowOn == 1_IB ) then
    !      write (*,'(4x,a)') '... Houston, We have a problem'
    !   end if
    !   yy_value = -999.0_RP
    !   IsKeepOn = 0_IB
    !   return
    !end if
    !
    !if ( count(xold_vec(1:nold_vec-1)-xold_vec(0:nold_vec-2) == 0) > 0 ) then
    !   do i=0,nold_vec-2
    !      if ( xold_vec(i) == xold_vec(i+1) ) then
    !         !write (*,*) xold_vec(i),xold_vec(i+1)
    !         !write (*,*) yold_vec(i),yold_vec(i+1)
    !
    !         if ( yold_vec(i) /= yold_vec(i+1) ) then
    !            IsKeepOn = 0_IB
    !            return
    !         end if
    !      end if
    !   end do
    !
    !end if
    
    !delta__x = 0.0_RP
    call Akima_Setup( xold_vec,yold_vec,nold_vec,p0,p1,p2,p3,delta__x )

    !zero_vec = 0.0_RP
    Is_Deriv = 0_IB
    Is_Index = 0_IB
    call Akimainterp( xx_value,yy_value,nxyvalue,xold_vec,nold_vec,p0,p1,  &
                      p2,p3   ,zero_vec,zero_vec,zero_vec,zero_vec,        &
                      zero_vec,zero_vec,zero_vec,zero_vec,dy_dxnew,        &
                      dy_dxold,dy_dyold,Is_Deriv,Is_Index )

    if ( IsShowOn == 1_IB ) then
       write (*,'(4x,a)') '[AkimaSpline]'
    end if
    
    return

END SUBROUTINE AkimaSpline
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SUBROUTINE author_AkimaSpline( a )
  use ModDataType

  implicit none
  
  character (len=21), intent(out) :: a

  !f2py intent(out) :: a

  a = 'Written by Jean Gomes'
  
END SUBROUTINE author_AkimaSpline
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! Jean@Porto - Tue Sep 27 18:38:40 AZOST 2011 +++++++++++++++++++++++++++++++

! *** Test ******************************************************************
!PROGRAM test
!END PROGRAM test
! *** Test ******************************************************************

! *** Number : 005                                                          !
!
! 1) ABS__smooth
! 2) Akima_Setup
! 3) Akimainterp
! 4) AkimaSpline
! 5) author_AkimaSpline
